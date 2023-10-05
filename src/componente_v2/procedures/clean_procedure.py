# Librerías necesarias
import pandas as pd
import numpy as np
from scipy import stats
from abc import ABC, abstractmethod
import argparse
import os
from datetime import datetime
import json
import sys
import requests

# Clase base para cualquier método de limpieza de datos
class DataCleaningMethod(ABC):

    @abstractmethod
    def clean(self, data):
        pass

# Implementación concreta para manejo de outliers
class ZScoreOutlierRemoval(DataCleaningMethod):
    
    def __init__(self, threshold=2):
        self.threshold = threshold

    def clean(self, data):
        z_scores = np.abs(stats.zscore(data))
        mask = (z_scores < self.threshold)
        data_processed = data[mask]
        return data_processed

# Implementación concreta para manejo de valores perdidos
class MeanImputation(DataCleaningMethod):

    def clean(self, data):
        return data.fillna(data.mean(), inplace=False)

# Clase de limpieza de datos que utiliza los métodos de limpieza definidos
class DataCleaner:

    def __init__(self, data_source_type, data_source):
        self.data_source_type = data_source_type
        if self.data_source_type == "csv":
            self.data_source = os.path.join(*data_source.split('/'))
        else:
            self.data_source = data_source
        
        self.data = self.load_data()
    
    def load_data(self):
        print("DATA SOURCE", self.data_source)
        if self.data_source_type == "csv":
            self.data = self.load_data_from_csv(self.data_source)
        elif self.data_source_type == "api":
            self.data = self.load_data_from_api(self.data_source)
        else:
            raise ValueError(f"Tipo de fuente de datos no reconocido: {self.data_source_type}")
        if self.data is None:
            raise Exception(f"No se pudo cargar los datos, {self.data_source_type}")

    def load_data_from_csv(self, file_path):
        """Carga los datos desde un archivo CSV"""
        try:
            return pd.read_csv(file_path, index_col=0)
        except FileNotFoundError:
            print(f"No se encontró el archivo en la ruta especificada: {file_path}")
            return None

    def load_data_from_api(self, url):
        """Carga los datos desde una API"""
        headers = {"Fiware-Service": "Testing"}
        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            print(f"Error al obtener datos de la API: {response.status_code}")
            return None
        data = response.json()
        df = pd.DataFrame(index=pd.to_datetime(data['index']))
        for attr in data['attributes']:
            if isinstance(attr['values'][0], dict):
                for key in attr['values'][0].keys():
                    column_name = f"{attr['attrName']}_{key}"
                    df[column_name] = [val[key] for val in attr['values']]
            else:
                df[attr['attrName']] = attr['values']
        return df

    def clean_data(self, cleaning_config):
        print("CLEAN DATA")
        """Limpia los datos usando la configuración de limpieza proporcionada"""
        cleaning_methods = {
            "ZScoreOutlierRemoval": ZScoreOutlierRemoval(threshold=3),
            "MeanImputation": MeanImputation()
        }
        print("data", self.data)

        for column, methods in cleaning_config.items():
            for cleaning_method in methods:
                self.data[column] = cleaning_methods[cleaning_method].clean(self.data[[column]])

    def save_clean_data(self, output_path):
        """Guarda los datos limpios en la ruta especificada"""
        if output_path is None:
            if self.data_source_type == "csv":
                base_name, ext = os.path.splitext(self.data_source)
                output_path = f"{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            elif self.data_source_type == "api":
                output_path = f"api_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            else:
                raise ValueError(f"Tipo de fuente de datos no reconocido: {self.data_source_type}")
        self.data.to_csv(output_path, index=True)

# Uso de la clase
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clean a dataset.')
    parser.add_argument('cleaning_config', type=str, help='Path al archivo JSON con la configuración de limpieza de datos')
    parser.add_argument('--output_path', type=str, help='Path donde se guardarán los datos limpios (opcional)')

    args = parser.parse_args()
    
    with open(args.cleaning_config, 'r') as f:
        cleaning_config = json.load(f)

    cleaner = DataCleaner(
        data_source_type=cleaning_config["data_source_type"],
        data_source=cleaning_config["data_source"]
    )

    cleaner.load_data()
    cleaner.clean_data(cleaning_config["cleaning_methods"])
    
    cleaner.save_clean_data(args.output_path) # TODO: Parametritzar
    sys.exit(0)

    # TODO Tots els prints/logs han de ser en format JSON, perquè es puguin interpretar per la crida
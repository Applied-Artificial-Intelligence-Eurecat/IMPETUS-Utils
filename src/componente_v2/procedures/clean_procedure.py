# Librerías necesarias
import pandas as pd
import numpy as np
from scipy import stats
from abc import ABC, abstractmethod
import argparse
import os
from datetime import datetime
import sys

# Clase base para cualquier método de limpieza de datos
class DataCleaningMethod(ABC):

    @abstractmethod
    def clean(self, data):
        pass

# Implementación concreta para manejo de outliers
class ZScoreOutlierRemoval(DataCleaningMethod):
    
    def __init__(self, threshold=3):
        self.threshold = threshold

    def clean(self, data):
        z_scores = np.abs(stats.zscore(data))
        return data[(z_scores < self.threshold).all(axis=1)]

# Implementación concreta para manejo de valores perdidos
class MeanImputation(DataCleaningMethod):

    def clean(self, data):
        return data.fillna(data.mean(), inplace=False)

# Clase de limpieza de datos que utiliza los métodos de limpieza definidos
class DataCleaner:

    def __init__(self, data_path, dataframe_column):
        self.data_path = data_path
        self.dataframe_column = dataframe_column
        self.data = self.load_data()
    
    def load_data(self):
        """Carga los datos desde el path proporcionado"""
        try:
            return pd.read_csv(self.data_path)[[self.dataframe_column]]
        except FileNotFoundError:
            print(f"No se encontró el archivo en la ruta especificada: {self.data_path}")
            return None

    def clean_data(self, cleaning_method):
        """Limpia los datos usando el método de limpieza proporcionado"""
        if not isinstance(cleaning_method, DataCleaningMethod):
            raise ValueError(f"cleaning_method debe ser una instancia de DataCleaningMethod, pero se obtuvo {type(cleaning_method)}")
        self.data = cleaning_method.clean(self.data)

    def save_clean_data(self, output_path):
        """Guarda los datos limpios en la ruta especificada"""
        self.data.to_csv(output_path, index=False)
        # print(f"Datos limpios guardados en: {output_path}")
        # print("{\"aaa\":1 }")


# Uso de la clase
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clean a dataset.')
    parser.add_argument('input_path', type=str, help='Path al archivo de datos', default="datasets\racha_max_manresa.csv")
    parser.add_argument('column_name', type=str, help='Name of the column to process')
    parser.add_argument('--output_path', type=str, help='Path donde se guardarán los datos limpios (opcional)')

    args = parser.parse_args()
    
    # Crear una instancia de la clase DataCleaner
    cleaner = DataCleaner(args.input_path, args.column_name)

    # Limpiar los outliers
    cleaner.clean_data(ZScoreOutlierRemoval(threshold=3))
    # Manejar los valores NaN
    cleaner.clean_data(MeanImputation())

    if args.output_path is None:
        base_name, ext = os.path.splitext(args.input_path)
        args.output_path = f"{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"

    # Guardar los datos limpios
    cleaner.save_clean_data(args.output_path) # TODO: Parametritzar
    sys.exit(0)

    # TODO Tots els prints/logs han de ser en format JSON, perquè es puguin interpretar per la crida
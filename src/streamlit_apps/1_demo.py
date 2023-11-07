import streamlit as st
import re
from itertools import groupby
from operator import itemgetter
import pandas as pd
from datetime import datetime
import sys
import json
import matplotlib.pyplot as plt
sys.path.insert(0, r'C:\Users\ian.palacin\Projectes\impetus-utils\src\componente_v2')
import procedures.clean_procedure as cp

variable_options = ["avg_speed", "max_wind_gust"]
# general_functions = ["Log10"]  # Tus funciones generales
general_functions = []  # Tus funciones generales
mask_generators = ["ZScoreOutlierMask"]  # Generadores de máscaras
mask_imputators = ["ZeroMaskImputation"]  # Imputadores específicos de máscaras

def parse_variable_form_to_method(data):
    values_to_variables = {0: "variable", 1: 'function', 2: 'imputator', 3:'arg'}
    variables_to_values = {y: x for x, y in values_to_variables.items()}

    elementwise_config = [[variables_to_values[key.split("_")[0]], int(key.split("_")[1]), int(key.split("_")[2])] for key in data.keys()]
    elementwise_config.sort(key = lambda row: (row[1],row[2], row[0]))
    elementwise_config = [ "_".join([values_to_variables[x],str(y),str(z)]) for [x,y,z] in elementwise_config ]
    arg_grouped_list, i = [], 0
    while i <= len(elementwise_config)-1:
        if i + 1 < len(elementwise_config) and 'arg_' in elementwise_config[i + 1]:
            arg_grouped_list.append([elementwise_config[i], elementwise_config[i + 1]])
            i += 1
        else:
            arg_grouped_list.append([elementwise_config[i]])
        i += 1

    final_list, i = [], len(arg_grouped_list)-1
    while i >= 0:
        if 'imputator' in arg_grouped_list[i][0]:
            final_list.append([arg_grouped_list[i-1], arg_grouped_list[i]])
            i -= 1
        else:
            final_list.append([arg_grouped_list[i]])
        i -= 1
    final_list = final_list[::-1]
    column = data[final_list[0][0][0]]
    methods = [[ [data[component_of_function] for component_of_function in function_with_args] for function_with_args in list_of_functions] for list_of_functions in final_list[1:]]
    return column, methods

def form_to_methods( data ):
    sorted_data = sorted(data.items(), key=lambda x: int(x[0].split('_')[1]))
    grouped_data = {k: dict(v) for k, v in groupby(sorted_data, key=lambda x: int(x[0].split('_')[1]))}
    return {variable_column: method_list for value in grouped_data.values() for variable_column, method_list in [parse_variable_form_to_method(value)]}

def draw_rows():
    for row_idx, cols in enumerate(st.session_state.rows):
        columns = st.columns(len(cols))

        for col_idx, col_info in enumerate(cols):
            if col_idx == 0:
                # Columna de selección de variables
                label, options, key = 'Variable', variable_options, f'variable_{row_idx}_0'
            else:
                # Columna de selección de funciones/transformaciones
                # Verificamos si la columna anterior fue un generador de máscaras y si es así,
                # establecemos las opciones a los imputadores de máscaras
                if cols[col_idx - 1]['selected'] in mask_generators:
                    label, options, key = 'Imputator', mask_imputators, f'imputator_{row_idx}_{col_idx}'
                    col_info['is_imputator'] = True  # Marcamos esta columna como un imputador
                else:
                    label, options, key = 'Function', general_functions + mask_generators, f'function_{row_idx}_{col_idx}'

            selected = columns[col_idx].selectbox(label, options, key=key, index=col_info.get('index', 0))
            st.session_state.rows[row_idx][col_idx]['selected'] = selected

            if selected in mask_generators:
                # Si la selección actual es un generador de máscaras y no hay una siguiente columna o no es un imputador
                if col_idx + 1 == len(cols) or not cols[col_idx + 1].get('is_imputator', False):
                    # Añadimos una nueva columna para la imputación de máscaras con las opciones de mask_imputators
                    st.session_state.rows[row_idx].append({'index': 0, 'selected': mask_imputators[0], 'is_imputator': True})
                    st.rerun()

            elif selected in general_functions:
                # Si se selecciona una función general y hay una columna de imputador de máscaras después, la eliminamos
                while col_idx + 1 < len(cols) and cols[col_idx + 1].get('is_imputator', False):
                    st.session_state.rows[row_idx].pop(col_idx + 1)
                    st.rerun()

            # Si no es ni un generador de máscaras ni una función general, pero hay una columna adicional que no corresponde, la eliminamos
            elif selected not in mask_generators + general_functions:
                if col_idx + 1 < len(cols) and cols[col_idx + 1].get('is_imputator', False):
                    st.session_state.rows[row_idx].pop(col_idx + 1)
                    st.rerun()

            # Caso especial para máscaras que requieren una entrada adicional (como ZScoreOutlierMask)
            if selected == "ZScoreOutlierMask":
                # Supongamos que 'ZScoreOutlierMask' requiere que el usuario introduzca un valor 'z'
                if 'z_value' not in col_info:
                    col_info['z_value'] = 3  # Valor por defecto
                z_key = f'arg_{row_idx}_{col_idx}'
                z_value = columns[col_idx].number_input('z', key=z_key, value=col_info['z_value'])
                st.session_state.rows[row_idx][col_idx]['z_value'] = z_value
# Función para añadir una nueva transformación o imputador
def add_new_transformation():
    # Añade un nuevo diccionario a la última fila existente con una función general por defecto
    st.session_state.rows[-1].append({'index': 0, 'selected': mask_generators[0], 'is_transformation': True})
    st.rerun()
# Función para añadir una nueva variable
def add_new_variable():
    # Añade una nueva fila que contiene un diccionario para una nueva variable
    st.session_state.rows.append([{'index': 0, 'selected': variable_options[0], 'is_variable': True}])
    st.rerun()

def form_configuration_logic():
    if 'rows' not in st.session_state:
        st.session_state.rows = [[{'index': 0, 'selected': variable_options[0]}]]
    draw_rows()
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Add new variable'):
            add_new_variable()
            st.rerun()
    with col2:
        if st.button('Add new transformation'):
            add_new_transformation()
            st.rerun()

    if st.button('Submit method'):
        st.write('Methods configured correctly!')
        form_result = st.session_state.to_dict()
        del form_result["rows"]
        del form_result["current_logic"]
        st.write(form_result)
        methods = form_to_methods(form_result)
        st.session_state.methods = methods
        st.session_state.current_logic = "date_selection"  # Marcar el formulario como enviado
        st.rerun()


def date_selection_logic():
    st.write("Please select the start and end dates:")
    col_start, col_end = st.columns(2)
    with col_start:
        start_time = st.date_input("Start time", datetime.now())
    with col_end:
        end_time = st.date_input("End time", datetime.now())

    # Verificar que la fecha de inicio no es posterior a la fecha de fin
    if start_time > end_time:
        st.error("Start time cannot be after end time. Please select a valid date range.")
    else:
        if st.button('Submit Dates'):
            # Aquí manejas la lógica de envío del segundo formulario
            # ... (procesar las fechas seleccionadas)
            st.success('Date range submitted successfully!')
            # Guardar las fechas en el estado de la sesión si es necesario
            st.session_state.start_time = start_time
            st.session_state.end_time = end_time
            st.session_state.current_logic = "data_retrieval"  # Marcar el formulario como enviado
            st.rerun()

def data_retrieval_logic():
    config_file = {
  "data_source_type": "api",
  "data_source": "https://data-manager.climate-impetus.eu/access/historical/entities",
  "api_additional_info":{
    "start_time":  "2019-09-14T00:00:00",
    "end_time": "2023-01-20T00:00:00",
    "entity_type": "windsensor",
    "format": "COLUMN",
    "origin": "DEVICE"}, 

  "methods": {
    "avg_speed": [ [["ZScoreOutlierMask", 2], ["ZeroMaskImputation"]] ],  
    "max_wind_gust":[]
        }
    }

    start_time = pd.to_datetime(st.session_state.start_time).strftime('%Y-%m-%dT%H:%M:%S')
    end_time = pd.to_datetime(st.session_state.end_time).strftime('%Y-%m-%dT%H:%M:%S')
    # config_file["api_additional_info"]["start_time"] = start_time
    # config_file["api_additional_info"]["end_time"] = end_time
    # config_file["methods"] = st.session_state.methods
    print(config_file)
    print("\n")

    st.session_state.config_file = config_file
    st.write(config_file)

    if st.button('Send payload to API'):
        st.session_state.current_logic = "raw_data_recieve_and_plot"  # Marcar el formulario como enviado
        st.rerun()
    
def send_payload_and_plot_data():
    config = st.session_state.config_file

    cleaner = cp.DataCleaner(data_source_type=config['data_source_type'], data_source=config['data_source'], config=config)
    df_pre_clean = cleaner.load_data_from_api(config['data_source'], config['api_additional_info'])
    st.dataframe(df_pre_clean)  
    st.line_chart(df_pre_clean)

    print(df_pre_clean)
    print(config)
    # cleaner.load_data()
    # cleaner.clean_data(config["methods"])
    # df_clean = cleaner.data



def main():
    if 'current_logic' not in st.session_state:
        st.session_state.current_logic = "method_configuration"  # Inicializar el estado del
        # st.session_state.current_logic = "date_selection"  # Inicializar el estado del

    if st.session_state.current_logic == "method_configuration":
        form_configuration_logic()
    elif st.session_state.current_logic == "date_selection":
        date_selection_logic()
    elif st.session_state.current_logic == "data_retrieval":
        data_retrieval_logic()
    elif st.session_state.current_logic == "raw_data_recieve_and_plot":
        send_payload_and_plot_data()


if __name__ == "__main__":
    main()





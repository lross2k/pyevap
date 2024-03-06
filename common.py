import tempfile, shutil, os, re

def get_cache_file_path() -> str | None:
    if os.name == 'nt':
        temp_file_path: str = tempfile.gettempdir() + '\\pyenv' + '\\.cache.csv'
        temp_file_path = temp_file_path.replace('\\', '/')
        return temp_file_path
    else:
        print('untested platform', os.name)
        return None

def save_result_to_system(file_path: str) -> None:
    if os.name == 'nt':
        temp_file_path: str = tempfile.gettempdir() + '\\pyenv' + '\\.cache.csv'
        temp_file_path = temp_file_path.replace('\\', '/')
        if not os.path.exists(temp_file_path):
            print('Cache file doesn\'t exist')
        else:
            final_file_path = file_path
            if not re.match(file_path, r'.+\.\w+$'):
                final_file_path += '.csv'
            shutil.copy(temp_file_path, final_file_path)
    else:
        print('untested platform', os.name)

def save_temp_to_system(data: list[str]) -> None:
    first_header: str = ";;Valores promedios;;;;;Valores mínimos;;;;;Valores máximos;;;;;Velocidad;Vapor de Saturación;;;Pendiente;Presión real de vapor derivada de la humedad realtiva;Déficit de ;RS (Rs );Dia;Distancia ;Declinación ;Ángulo de radición horario;;;;;;Radiación extraterrestre;Duración máxima;R so;Radiación ;Radiación;Radiación ;Radiación;Flujo de calor del suelo;Cálculo de ET"
    second_header: str = "Día;Número de días;TA;HR;VV;RS (Rs );PR;TA;HR;VV;RS (Rs );PR;TA;HR;VV;RS (Rs );PR;Viento a 2 m;e°(Tmax);e°(Tmin);Presión media;Curva de sarturación;presión real;presión de vapor;Radiación solar ;juliano;relativa;solar;Valor ;Correción seccional;puesta de sol;sol punto medio;inicio;final;Ra;Insolación;día despejado;onda corta (Rns);relativa;onda larga (Rnl);neta (Rn);G;ET"
    third_header: str = ";;grados C;%;m/s;W/m2;grados C;grados C;%;m/s;W/m2;grados C;grados C;%;m/s;W/m2;grados C;u2 (m/2);kPa;kPa;es (kPa);Δ (kPa/ C°1);ea (kPa);es - ea (kPa);MJ/ m^(2)* dia;J;dr;δ;b;Sc;ωs ;ω;ω1;ω2;MJ /m^(2) *dia;N;MJ/ m^(2)* dia;MJ/ m^(2)*día;Rs/Rso;MJ/ m^(2) *día;MJ/ m^(2) *dia;MJ/ m^(2)*dia;mm/dia"
    if os.name == 'nt':
        temp_directory: str = tempfile.gettempdir() + '\\pyenv'
        temp_file_path: str = temp_directory + '\\.cache.csv'
        os.makedirs(temp_directory, exist_ok=True)
        with open(temp_file_path, 'w', encoding='utf-8') as cache_file:
            cache_file.write(first_header+'\n')
            cache_file.write(second_header+'\n')
            cache_file.write(third_header+'\n')
            for line in data:
                cache_file.write(line+'\n')
    else:
        print('untested platform', os.name)

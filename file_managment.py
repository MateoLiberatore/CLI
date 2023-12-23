import logging,os,glob


def find_file(nombre_archivo):

    pattern = f"**/{nombre_archivo}"
    archivos_encontrados = glob.glob(pattern, recursive=True)

    if archivos_encontrados:
        return archivos_encontrados[0]
    else:
        return 'file not found'
    

def delete_file(filepath):
    try:
        os.remove(filepath)
        logging.info("Deleted File: %s", filepath)
    except FileNotFoundError:
        logging.info("File not found %s", filepath)
    except PermissionError:
        logging.info("Permission not granted: %s", filepath)
    except Exception as e:
        logging.error("Error: %s", str(e))

def scan_files():
    
    current_directory = os.getcwd()
    sub_directory_name = "reports"
    sub_directory_path = os.path.join(current_directory, sub_directory_name)

    if os.path.exists(sub_directory_path) and os.path.isdir(sub_directory_path):
        print(f"The subdirectory '{sub_directory_name}' exists in the current directory.")

        # Display files in the subdirectory
        files_in_reports = os.listdir(sub_directory_path)
        
        if files_in_reports:
            print("Files in the 'reports' subdirectory:")
            for i, file in enumerate(files_in_reports, 1):
                print(f"{i}. {file}")
                
            # Ask the user to select files
            selection = input("Enter the number/numbers of the files you want to select (separated by space): ").split()
            # Process user selection
            selected_indices = [int(index) for index in selection if 1 <= int(index) <= len(files_in_reports)]
            selected_files = [os.path.join(sub_directory_path, files_in_reports[index-1]) for index in selected_indices]
            
            if selected_files:
                print("Selected files:")
                for file in selected_files:
                    print(file)
                return tuple(selected_files)
            else:
                print("Invalid selection.")
        else:
            print("The 'reports' subdirectory is empty.")
    else:
        print(f"The subdirectory '{sub_directory_name}' does not exist in the current directory.")



def reports_folder():
    actual_directory = os.getcwd()
    folder_name = "reports"
    path = os.path.join(actual_directory, folder_name)

    try:
        # Try to create the folder
        os.makedirs(path)
        print(f"Carpeta '{folder_name}' creada en: {path}")
    except FileExistsError:
        print(f"La carpeta '{folder_name}' ya existe en: {path}")

    return path
    
def delete_files():

    files = scan_files()

    for path in files:
        
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"Archivo eliminado: {path}")
            except OSError as e:
                print(f"No se pudo eliminar el archivo {path}: {e}")
        else:
            print(f"El archivo no existe en la ruta proporcionada: {path}")


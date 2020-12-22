import datetime
def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d/%m/%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be DD/MM/YYYY")
        
allowed_items_dict = {
    'acquisition_mode': ['Draft', 'Asta', 'Algoritmo', 'Acquisto', 'Scambio', 'Svincolo', ''],
    'owner': ['luca', 'pietro', 'enzo', 'nanni', 'mario', 'musci8', 'franky', ''],
    'squad': ['main', 'primavera', ''],
    'on_loan': [True, False],
    'FC_role': ['P', 'D', 'C', 'A'],
}
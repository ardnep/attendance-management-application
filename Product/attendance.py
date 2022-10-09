from filemanager import FileManager
from users import User


class Attendance:
    @staticmethod
    def take_new(name_of_record, names_of_students):
        processed_names = FileManager.process_names(names_of_students)
        validation_result = Attendance.validate_input(name_of_record, processed_names)
        if validation_result == 'Successful!':
            FileManager.create_excel_file(names_of_students, name_of_record)
            return 'Successful!'

        return validation_result

    @staticmethod
    def update(name_of_record, chat_file):
        if '.txt' not in chat_file:
            return 'Upload a chat file and try again!'

        validation_result = Attendance.validate_input(name_of_record)
        if validation_result == 'Successful!':
            try:
                excel_file = FileManager.find_file(f"{name_of_record}", path=f'users/{User.current_user}', specific=True)[0]
                FileManager.update_excel_file(chat_file, excel_file)
                return 'Successful!'
            except IndexError:
                return 'No matching files found!'

        return validation_result

    @staticmethod
    def add_students(name_of_record, names_of_students):
        processed_names = FileManager.process_names(names_of_students)
        validation_result = Attendance.validate_input(name_of_record, processed_names)
        if validation_result == 'Successful!':
            try:
                excel_file = FileManager.find_file(name_of_record, path=f'users/{User.current_user}', specific=True)[0]
                FileManager.add_students_excel(names_of_students, excel_file)
                return 'Successful!'
            except IndexError:
                return 'No matching files found!'

        return validation_result

    @staticmethod
    def remove_students(name_of_record, names_of_students):
        processed_names = FileManager.process_names(names_of_students)
        validation_result = Attendance.validate_input(name_of_record, processed_names)
        if validation_result == 'Successful!':
            try:
                excel_file = FileManager.find_file(name_of_record, path=f'users/{User.current_user}', specific=True)[0]
                FileManager.remove_students_excel(names_of_students, excel_file)
                return 'Successful!'
            except IndexError:
                return 'No matching files found!'

        return validation_result

    @staticmethod
    def validate_input(*inputs_to_validate):
        for inputs in inputs_to_validate:
            if type(inputs) == list:
                if any(values for values in inputs if not values.isalpha()):
                    return 'Names can only contain letters!'

            else:
                if inputs.isspace():
                    return 'Input something and try again!'

                if not inputs.isalnum():
                    return 'Field can only contain letters and numbers!'

        return 'Successful!'

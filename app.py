from flask import Flask, request, render_template, redirect, url_for
import csv
import os

app = Flask(__name__)

# Define the mandatory fields based on your form's input names
mandatory_fields = [
    'user_name','set_number', 'total_sets', 'special_study_number_top', 
    'special_study_number', 'number_of_plates', 'sample_id_range', 
    'goal_of_study', 'new_sample_id_range_split', 'user_dropped', 
    'date_dropped', 'user_transferred', 'date_transferred', 
    'new_sample_id_range_separation', 'standard_operating_procedure', 
    'standard_lot_number', 'extraction_buffer', 'dilution_buffer', 
    'liquid_transfer_machine_id', 'changes_to_procedure', 
    'date_of_drop_off', 'drop_off_location'
]


csv_file_path = '/home/vikas/pdf_form_flask/data.csv'  
if not os.path.isfile(csv_file_path):
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(mandatory_fields)

@app.route('/', methods=['GET', 'POST'])
def form1_1():
    error_message = None
    success_message = None
    try:
        if request.method == 'POST':
            # Collecting form data as it is
            form_data = {field: request.form.get(field).strip() for field in mandatory_fields}

            if not all(form_data.values()):
                error_message = 'Please fill out all the fields.'
            else:
                # Check for unique user_name
                with open(csv_file_path, 'r') as file:
                    existing_user_names = [row[0] for row in csv.reader(file)]
                    if form_data['user_name'] in existing_user_names:
                        error_message = 'User name already exists. Please use a different user name.'
                        return render_template('form1_1.html', error_message=error_message)

                # Rearranging the data to put user_name first
                ordered_data = [form_data['user_name']] + [form_data[field] for field in mandatory_fields if field != 'user_name']

                # Write rearranged data to CSV
                with open(csv_file_path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(ordered_data)

                success_message = 'Form has been successfully submitted.'
                return render_template('form1_1.html', success_message=success_message)

        return render_template('form1_1.html', error_message=error_message, success_message=success_message)
    except Exception as e:
        print("An error occurred:", e)
        return "An error occurred. Check server logs."


if __name__ == '__main__':
    print("Current working directory:", os.getcwd())
    app.run(host='0.0.0.0', port=5000, debug=True)

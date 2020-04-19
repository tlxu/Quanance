import os
import win32com.client
import re

print("Python to retrieve attachemnts from outlook")

# outlook message file
msg_file_relative_dir = '.\\cibc_mellon_ald'
msg_file_suffix = '.msg'

# attached csv file will be saved as ALD_REPORT-DD-MMM-YYY.csv
csv_file_prefix = 'ALD_REPORT'
csv_file_relative_dir = '.\\csv'

# use absolute path, or you'll get error later on
msg_file_dir = os.path.abspath(msg_file_relative_dir)
csv_file_dir = os.path.abspath(csv_file_relative_dir)

# msg_files = [f for f in os.listdir(msg_file_dir) if msg_file_suffix in f]
msg_files = []
print(msg_file_dir)
for r, d, f in os.walk(msg_file_dir):
    for file in f:
        if '.msg' in file:
            msg_files.append(os.path.join(r, file))

number_of_files = len(msg_files)
for idx, file in enumerate(msg_files):
    # get file date 02-Apr-2020
    print(f'{idx+1}/{number_of_files}: {file}')
    date_str = re.split(' |\.', file)[-2]
    print(date_str)

    # Read attachments
    outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
    msg = outlook.OpenSharedItem(file)
    att = msg.Attachments
    for i in att:
        csv_file_name = os.path.join(csv_file_dir, f'{csv_file_prefix}-{date_str}.csv')
        i.SaveAsFile(csv_file_name)

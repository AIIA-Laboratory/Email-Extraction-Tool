## Email Extraction Tool

This CLI tool scans through .OST and .PST files looking for unique email accounts. 

The [library](https://pypi.org/project/libpff-python/) used is an wrapper of the libpff Linux package. The current DFS search implementation was based upon this [script](https://github.com/PacktPublishing/Learning-Python-for-Forensics/tree/master/Chapter%2010) since there are little to no documentation of the wrapper as well as the libpff package itself.

The wrapper doesn't give access to *TO*, *CC*, *BCC* header thus the script looks for email addresses in the *transport_headers* in result gathering email and hop servers as well that will have to be cleaned afterwards.

A Windows executable can be found at `dist/main.exe` that was created using the `pyinstaller` library. 


### Run the script
Go to the directory that the script resides to and open a terminal windows, either `cmd` or `powershell` by (*CTRL + Shift + Right Click* in Windows.)

Then run stript with the command below:

```bash
./main.exe --file dir --year YEAR
```
where dir defines the path to the mail box file and year the low bound of a time period that we want to scrape emails from.

Upon execution a file named `email_addresses.csv` is created at the current working directory. 

**Suggested:** call the script from the same directory that is stored.

Due to DFS search progress of the task is not shown.

### Creating a new executable

You can create a new executable by running the command below.

```cmd
pyinstaller --onefile --console main.py
```

### Notes
* The script has been tested on limited encodings. On exceptions the code just ignores emails causing non addressed issues.
* In the case where more advanced features and functionality is needed in future implementations, it is suggested to look into the [pywin32](https://pypi.org/project/pywin32/) library.

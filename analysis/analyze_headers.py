import os
import re
import pandas as pd
from astropy.time import Time

def extract_value(header_text, key):
    """
    Extracts the value of a given keyword from a header string using regex.

    Parameters:
        header_text (str): The content of the header file as a string.
        key (str): The FITS keyword to search for.

    Returns:
        str or None: The value of the keyword, if found.
    """
    pattern = re.compile(rf"{re.escape(key)}\s*=\s*'?([^\n']+)'?")
    match = pattern.search(header_text)
    return match.group(1).strip() if match else None

def analyze_single_header(file_path):
    """
    Analyzes a single FITS header text file and extracts selected metadata.

    Parameters:
        file_path (str): Full path to the .fits_header.txt file.

    Returns:
        dict: Extracted metadata including wavelength range and object info.
    """
    with open(file_path, "r") as f:
        text = f.read()

    try:
        crval1 = float(extract_value(text, "CRVAL1"))
        cdelt1 = float(extract_value(text, "CDELT1"))
        naxis1 = int(extract_value(text, "NAXIS1"))
        lambda_start = crval1
        lambda_end = crval1 + cdelt1 * (naxis1 - 1)
    except (TypeError, ValueError):
        lambda_start = lambda_end = None

    return {
        "File": os.path.basename(file_path),
        "Object": extract_value(text, "OBJECT"),
        "Type": extract_value(text, "IMAGETYP"),
        "Instrument": extract_value(text, "INSTRUME"),
        "Observation Mode": extract_value(text, "HIERARCH ESO PRO REC1 FIBRE NAME"),
        "Status": "processed" if "HISTORY" in text else "unknown",
        "Lambda_start (Å)": round(lambda_start, 2) if lambda_start else None,
        "Lambda_end (Å)": round(lambda_end, 2) if lambda_end else None
    }

def analyze_headers_in_directory(directory):
    """
    Processes all `.fits_header.txt` files in a given directory.

    Parameters:
        directory (str): Path to the folder containing header text files.

    Returns:
        pd.DataFrame: Table summarizing the extracted metadata.
    """
    header_files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(".fits_header.txt")
    ]

    results = [analyze_single_header(f) for f in header_files]
    return pd.DataFrame(results)

def analyze_headers_dict(headers_dict):
    """
    Processes a dictionary of FITS headers and extracts metadata from each.

    Parameters:
        headers_dict (dict): Dictionary with file names as keys and FITS headers as values.

    Returns:
        pd.DataFrame: Summary table with object, wavelength, status, and Julian Date.
    """
    results = []

    for file_name, header in headers_dict.items():
        crval1 = header.get("CRVAL1")
        cdelt1 = header.get("CDELT1")
        naxis1 = header.get("NAXIS1")

        try:
            lambda_start = float(crval1)
            lambda_end = float(crval1) + float(cdelt1) * (int(naxis1) - 1)
        except (TypeError, ValueError):
            lambda_start = lambda_end = None

        date_obs = header.get("DATE-OBS")
        ut = header.get("UT")

        try:
            if date_obs and ut:
                datetime_str = f"{date_obs.strip()} {ut.strip()}"
                jd = Time(datetime_str, format="iso", scale="utc").jd
            else:
                jd = None
        except Exception:
            jd = None

        result = {
            "File": file_name,
            "Object": header.get("OBJECT"),
            "Type": header.get("IMAGETYP"),
            "Instrument": header.get("INSTRUME"),
            "Observation Mode": header.get("HIERARCH ESO PRO REC1 FIBRE NAME"),
            "Status": "processed" if "HISTORY" in header else "unknown",
            "Lambda_start (Å)": round(lambda_start, 2) if lambda_start else None,
            "Lambda_end (Å)": round(lambda_end, 2) if lambda_end else None,
            "Julian Date": jd
        }

        results.append(result)

    return pd.DataFrame(results)
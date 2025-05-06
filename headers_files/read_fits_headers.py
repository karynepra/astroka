from pathlib import Path
from astropy.io import fits
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)

def scan_directories(directories: List[str]) -> List[str]:
    """
    Scans a list of directories and returns a list of full paths of FITS files found.

    Parameters:
        directories (List[str]): List of directory paths to scan.

    Returns:
        List[str]: List of full paths to the FITS files found.
    """
    fits_files = []
    for directory in directories:
        path = Path(directory)
        if path.is_dir():
            fits_files.extend([str(f) for f in path.glob("*.fits") if f.is_file()])
    return fits_files

def extract_headers(fits_files: List[str]) -> Dict[str, fits.Header]:
    """
    Extracts headers from a list of FITS files.

    Parameters:
        fits_files (List[str]): List of paths to FITS files.

    Returns:
        Dict[str, fits.Header]: Dictionary with filenames as keys and headers as values.
    """
    headers = {}
    for file in fits_files:
        try:
            header = fits.getheader(file, hdu=0)
            headers[file] = header
        except Exception as e:
            logging.error(f"❌ Error reading {file}: {e}")
    return headers

def build_data_list(headers: Dict[str, fits.Header], desired_keys: List[str]) -> List[Dict[str, Any]]:
    """
    Builds a list of dictionaries with selected header values.

    Parameters:
        headers (Dict[str, fits.Header]): Dictionary of FITS headers.
        desired_keys (List[str]): List of header keys to extract.

    Returns:
        List[Dict[str, Any]]: List of dictionaries with filename and selected header values.
    """
    data_list = []
    for filename, header in headers.items():
        data = {"Filename": filename}
        for key in desired_keys:
            data[key] = header.get(key, None)
        data_list.append(data)
    return data_list
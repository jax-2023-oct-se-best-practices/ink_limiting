# Ink limit module
from PIL import Image
import numpy as np
import sys
from typing import Callable, Tuple

def ink_limit_proportional(arr: np.ndarray, inkLimit: float = 240.) -> np.ndarray:
    """
    Do proportional reduction using numpy's operators

    Args:
        arr (np.ndarray): Input array

    Returns:
        np.ndarray: Output array
    """
    assert arr.shape[2] == 4
    assert arr.dtype in np.uint8
    totals = np.sum(arr, axis = -1, keepdims=True)
    # TODO: implement proportional reduction here
    return arr

def ink_limit_ucr(arr: np.array, inkLimit: float = 240.) -> np.array:
    """
    Do the UCR ink reduction using numpy ops
    """
    assert arr.shape[2] == 4
    assert arr.dtype == np.uint8
    totals = np.sum(arr, axis = -1, keepdims=True)
    # TODO: implement UCR-based ink limiting here
    return arr

help_text = """\
command line: python <input_file> <output_file> [<ink_limit>] [<method>]
  method = 0: use proportional ink reduction
  method = 1: use under color removal ink limiting
"""
def help():
    print(help_text)

def applyInkLimit(inName: str,
                  outName: str,
                  inkLimiter: Callable,
                  limit: float) -> Tuple[int, int]:
    inimg = Image.open(inName, "r")
    arr = np.asarray(inimg)
    outarr = inkLimiter(arr, limit)
    total_pixels = arr.shape[0]*arr.shape[1]
    outimg = Image.fromarray(outarr, mode="CMYK")
    outimg.save(outName, compression="tiff_deflate")

if __name__ == "__main__":
    limit = 240.
    method = 0
    if len(sys.argv) > 3:
        limit = float(sys.argv[3])
    if len(sys.argv) > 4:
        method = int(sys.argv[4])
    if method == 0:
        inklimiter = ink_limit_proportional
    elif method == 1:
        inklimiter = ink_limit_ucr
    else:
        help()
        exit(1)
    infilename = sys.argv[1]
    outfilename = sys.argv[2]
    applyInkLimit(infilename,
                  outfilename,
                  inklimiter,
                  limit)
    print("Done!")

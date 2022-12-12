import csv
import os
import time 
import resource

from concurrent.futures import ThreadPoolExecutor, as_completed

from multiprocessing import Pool

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def get_memory():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  / 1024

def apply_formula(data: dict) -> dict:
    """
    this project helps to calculate the formula
    """

    context = {}

    game_number = int(data["game_number"])
    game_length = int(data["game_length"])

    # initialize with object
    context["game_number"] = game_number
    context["game_length"] = game_length

    # calcuatet he multiplication
    context["game_mul"] = game_number * game_length

    # calculate the add
    context["game_add"] = game_number + game_length

    # calculate the add
    context["game_sub"] = game_length - game_number

    # calculate div
    context["game_div"] = game_length / game_number

    # complex multiplication
    context["game_pow"] = pow(game_number, game_length)

    # there some other cpu intensive task in this
    time.sleep(0.0001)

    return context


def apply_formula2(data: dict) -> dict:
    """
    this project helps to calculate the formula
    """

    context = {}

    game_number = int(data["game_number"])
    game_length = int(data["game_length"])

    # initialize with object
    context["game_number"] = game_number
    context["game_length"] = game_length

    # calcuatet he multiplication
    context["game_mul"] = game_number * game_length

    # calculate the add
    context["game_add"] = game_number + game_length

    # calculate the add
    context["game_sub"] = game_length - game_number

    # calculate div
    context["game_div"] = game_length / game_number

    # complex multiplication
    context["game_pow"] = pow(game_number, game_length)

    return context


def normal_parse(file_path: str, func) -> list:
    output = []
    start_time = time.time()
    start_memory = get_memory()
    with open(file_path, "r") as reader:
        csv_file = csv.DictReader(reader)
        for row in csv_file:
            output.append(func(row))
    time_stamp = round(time.time() - start_time, 6)
    return [output,time_stamp,get_memory()]


def using_threads(file_path: str, func) -> list:
    output = []
    start_time = time.time()
    start_memory = get_memory()
    with open(file_path, "r") as reader:
        csv_file = csv.DictReader(reader)
        # applying concurrences
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_obj = {executor.submit(func, row) for row in csv_file}
            for future in as_completed(future_obj):
                output.append(future.result())
    time_stamp = round(time.time() - start_time, 6)
    return [output,time_stamp,get_memory()]


def using_multi_cores(file_path: str, func):
    output = []
    start_time = time.time()
    start_memory = get_memory()
    with open(file_path, "r") as reader:
        csv_file = csv.DictReader(reader)
        data = [row for row in csv_file]
        # applying concurrences
        with Pool(5) as p:
            output = p.map(func, data)

    time_stamp = round(time.time() - start_time, 6)
    return [output,time_stamp,get_memory()]


def upload_file_to_path(file) -> str:
    """
    helps to upload the path and return


    Args:
        file (_type_): _description_

    Returns:
        str: _description_
    """

    return default_storage.save(
        f"tmp/{time.time()}-{file.__str__()}",
        ContentFile(file.read()),
    )





context_provider = {
    1: [
        normal_parse,
        apply_formula,
        "Normal Parsers",
        "Will Parse the file using normal iteration and and normal function with delay in computation",
    ],
    2: [
        using_threads,
        apply_formula,
        "Using Thread",
        "Will Parse the file using Thread and normal function with delay in computation",
    ],
    3: [
        using_multi_cores,
        apply_formula,
        "Using Multi Processing",
        "Will Parse the file using Multi Processing and normal function with delay in computation",
    ],
    4: [
        normal_parse,
        apply_formula2,
        "Normal Parsers",
        "Will Parse the file using normal iteration and and function without delay in computation",
    ],
    5: [
        using_threads,
        apply_formula2,
        "Using Thread",
        "Will Parse the file using normal iteration and and function without delay in computation",
    ],
    6: [
        using_multi_cores,
        apply_formula2,
        "Using Multi Processing",
        "Will Parse the file using normal iteration and and function without delay in computation",
    ],
}


if __name__ == "__main__":
    start = get_memory()
    normal_parse(
        "/media/sheggamharshith/new partition/csi/parallel_computing/csvreader/reader/data/50k.csv",
        apply_formula2,
    )
    print(get_memory() - start)

    using_threads(
        "/media/sheggamharshith/new partition/csi/parallel_computing/csvreader/reader/data/50k.csv",
        apply_formula2,
    )
    print(get_memory() - start)

    using_multi_cores(
        "/media/sheggamharshith/new partition/csi/parallel_computing/csvreader/reader/data/50k.csv",
        apply_formula2,
    )
    print(get_memory() - start)

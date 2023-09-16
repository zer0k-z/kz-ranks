import numpy as np

def format_seconds(seconds):
    # Format: (hh:)mm:ss.ms
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    seconds, milliseconds = divmod(seconds, 1)
    milliseconds = int(milliseconds * 1000)  # Convert to milliseconds

    if hours > 0:
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{milliseconds:03d}"
    else:
        return f"{int(minutes):02d}:{int(seconds):02d}.{milliseconds:03d}"

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def sanitize_name_md(name):
    # Make names with | not break the table.
    return name.replace('|', r'\|')

def make_markdown_table(map_name, array):

    """ Input: Map name, python list with rows of table as lists
               First element as header. 
        Output: String to put into a .md file, only the first 100 lines
    """

    markdown = f"# {map_name} Maptop\n"
    markdown += "\n" + str("| ")

    for e in array[0]:
        to_add = " " + str(e) + str(" |")
        markdown += to_add
    markdown += "\n"

    markdown += '|'
    for _ in range(len(array[0])):
        markdown += str("-------------- | ")
    markdown += "\n"

    for entry in array[1:100]:
        markdown += str("| ")
        for e in entry:
            to_add = str(e) + str(" | ")
            markdown += to_add
        markdown += "\n"

    return markdown + "\n"

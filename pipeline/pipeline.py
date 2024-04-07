from data.dataloader import load_data
from component.ingest import convert_data_to_vector
from component.chunk import chunk
import sys

def main():
    arg = sys.argv[1]
    match arg:    
        case "ingest":
            convert_data_to_vector(load_data())
            return
        case "chunk":
            chunk(load_data())
            return
        case default:
            print(f"Invalid argument: {arg} - Only allowed: [ingest, chunk]")
            return
    
if __name__ == "__main__":
    main()

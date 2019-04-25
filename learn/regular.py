import re

def main():
    msg = '010 12345678'
    dd = re.match('\d{3}\s+\d{8}',msg)
    print(dd)

if __name__ == '__main__':
    main()
    
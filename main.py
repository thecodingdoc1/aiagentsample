from db_setup import create_db
from agent import call_agent

def main():
    create_db()
    call_agent()

if __name__ == "__main__":
    main()
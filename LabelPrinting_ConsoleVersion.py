import LabelPrinting_Backend as backend

def main():
    baseUrl, headers, baseDir = backend.initialize()

    while True:
        # Prompt user for Service Ticket # and exit if they type "end"
        userInput = input("Enter Service Ticket # (Start with \'L\' for laptops): ")
        ticketNumberInput = userInput.replace("L", "").strip()

        if ticketNumberInput.lower() == "end":
            break
        
        # Ensure ticket number is exactly 7 digits
        if not (ticketNumberInput.isdigit() and len(ticketNumberInput) == 7):
            print("Error: Ticket number must be exactly 7 digits.")
            continue

        backend.process_ticket(baseUrl, headers, baseDir, ticketNumberInput, laptop = userInput.startswith("L"))

if __name__ == "__main__":
    main()
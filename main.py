from dispatcher import dispatch

if __name__ == "__main__":
    user_input = {
        "agent": "invoice_reader",
        "params": {"image_path": "data/invoice.jpg"}
    }
    result = dispatch(user_input)
    print("Výsledek:\n", result)
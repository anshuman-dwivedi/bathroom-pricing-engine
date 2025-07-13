def get_vat_rate(task_name, city):
    # For simplicity, apply a flat 20% VAT across all services
    # This can be extended per city/task in the future
    return 0.20
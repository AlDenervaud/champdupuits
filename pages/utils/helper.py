import pandas as pd

def UpdateOrderFinal(order):
    # Reset Total column
    if "Total" in order.columns:
        order.drop("Total", axis=1, inplace=True)
    # Remove row with grand total
    order = order[order["Nom"].str.strip() != ""]
    
    # Updates total price based on price and quantity
    order["price_temp"] = order["Prix"].apply(lambda x: float(x.split(" ")[0].replace(",", ".")))
    order["Quantité"] = pd.to_numeric(order["Quantité"], errors='coerce')
    order["Total"] = order["price_temp"] * order["Quantité"]
    
    # Remove items with 0 quantity
    order = order[order["Quantité"] != 0]
    
    # Add grand total
    order = order._append({"Nom":"", "Prix":"", "Catégorie":"", "Quantité":"", "Total":order["Total"].sum()}, ignore_index=True)
    order["Total"] = order["Total"].apply(lambda x: "{:.2f} €".format(x))

    # Cleaning
    final_order = order[['Nom', 'Prix', 'Catégorie', 'Quantité', 'Total']]

    return final_order

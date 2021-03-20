def lorem_ipsum(product):
    product.title = "title{}".format(product.sku)
    product.description = "description{}".format(product.sku)
    product.price = "price{}".format(product.sku)
    product.img_src = "https://img.src/{}".format(product.sku)

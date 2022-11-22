from user_agents import parse


def get_device(ua):
    ua = parse(ua)

    friendly_brands = {"Huawei": "华为", "OnePlus": "一加", "Apple": "苹果",
                       "XiaoMi": "小米", "SAMSUNG": "三星", "Lenovo": "联想", "Nokia": "诺基亚",
                       "Sony": "索尼", "Generic_Android": "安卓"}
    friendly_models = {"SEA-AL10":"nova 5 Pro", "iOS-Device":""}
    brand = ua.device.brand

    if ua.device.model is None:
        model = ""
    else:
        model = ua.device.model

    if brand == "Generic_Android":
        if model == "XQ-AT52":
            brand = "Sony"
    
    if model.startswith(brand):
        model = model[len(brand):].strip()

    brand = friendly_brands.get(brand, brand)
    model = friendly_models.get(model, model)

    device = f"{brand}{model}"
    return device

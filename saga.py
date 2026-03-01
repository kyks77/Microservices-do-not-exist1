
class Step:
    def __init__(self, name, do, compensate):
        self.name = name
        self.do = do
        self.compensate = compensate

def run_saga(steps, ctx):
    completed = []
    try:
        for step in steps:
            step.do(ctx)
            completed.append(step)
        return True, None
    except Exception as e:

        for step in reversed(completed):
            try:
                step.compensate(ctx)
            except Exception:
                pass
        return False, e

def payment_do(ctx):
    ctx["payment_id"] = "pay_001"
    ctx["payment_captured"] = True

def payment_comp(ctx):
    if ctx.get("payment_captured"):
        ctx["payment_refunded"] = True
        ctx["payment_captured"] = False

def inventory_do(ctx):
    ctx["reservation_id"] = "res_001"
    ctx["inventory_reserved"] = True

def inventory_comp(ctx):
    if ctx.get("inventory_reserved"):
        ctx["inventory_released"] = True
        ctx["inventory_reserved"] = False

def shipping_do(ctx):
    raise RuntimeError("shipping provider down")

def shipping_comp(ctx):
    if ctx.get("shipping_created"):
        ctx["shipping_cancelled"] = True
        ctx["shipping_created"] = False

if __name__ == "__main__":
    ctx = {"order_id": "order_123"}

    steps = [
        Step("Payment", payment_do, payment_comp),
        Step("Inventory", inventory_do, inventory_comp),
        Step("Shipping", shipping_do, shipping_comp),
    ]

    ok, err = run_saga(steps, ctx)

    print("OK:", ok)
    if err:
        print("ERROR:", err)
    print("CTX:", ctx)
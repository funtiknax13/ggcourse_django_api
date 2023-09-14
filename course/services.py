import stripe

from config.settings import STRIPE_KEY

stripe.api_key = STRIPE_KEY


def create_payment(obj, product_price):
  try:
    product = stripe.Product.create(name=obj.title)
    price = stripe.Price.create(
      unit_amount=product_price,
      currency="usd",
      product=product['id'],
    )
    session = stripe.checkout.Session.create(
      success_url="http://127.0.0.1:8000/",
      line_items=[
        {
          "price": price["id"],
          "quantity": 1,
        },
      ],
      mode="payment",
    )
    return session["url"]
  except Exception as inst:
    print(inst)
    return False

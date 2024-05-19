import yookassa
from settings import YOOKASSA_API_ID, YOOKASSA_API_KEY, BOT_LINK


def create_payment(price: int):
    yookassa.Configuration.account_id = YOOKASSA_API_ID
    yookassa.Configuration.secret_key = YOOKASSA_API_KEY

    payment = yookassa.Payment.create({
        "amount": {
            "value": price,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": BOT_LINK
        },
        "description": "Платеж принят",
        "capture": True
    })

    url = payment.confirmation.confirmation_url

    return url, payment


def payment_check(id):
    payment = yookassa.Payment.find_one(id)
    if payment.status == 'succeeded':
        return True
    return False

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.urls import reverse
import stripe
from .models import Item, Order


def get_stripe_key_for_currency(currency):
    """Get Stripe secret key for the given currency"""
    if currency == 'eur':
        return settings.STRIPE_SECRET_KEY_EUR
    return settings.STRIPE_SECRET_KEY_USD


def get_stripe_publishable_key_for_currency(currency):
    """Get Stripe publishable key for the given currency"""
    if currency == 'eur':
        return settings.STRIPE_PUBLISHABLE_KEY_EUR
    return settings.STRIPE_PUBLISHABLE_KEY_USD


def create_checkout_session_for_item(item):
    """Create Stripe checkout session for an item"""
    stripe.api_key = get_stripe_key_for_currency(item.currency)
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': int(item.price * 100),  # Convert to cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=settings.SITE_URL.rstrip('/') + reverse('success'),
        cancel_url=settings.SITE_URL.rstrip('/') + reverse('cancel'),
    )
    return session


def create_checkout_session_for_order(order):
    """Create Stripe checkout session for an order"""
    stripe.api_key = get_stripe_key_for_currency(order.currency)
    
    line_items = []
    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': int(item.price * 100),  # Convert to cents
            },
            'quantity': 1,
        })
    
    session_params = {
        'payment_method_types': ['card'],
        'line_items': line_items,
        'mode': 'payment',
        'success_url': settings.SITE_URL.rstrip('/') + reverse('success'),
        'cancel_url': settings.SITE_URL.rstrip('/') + reverse('cancel'),
    }
    
    # Add discount if available
    if order.discount and order.discount.stripe_coupon_id:
        session_params['discounts'] = [{'coupon': order.discount.stripe_coupon_id}]
    elif order.discount:
        # Create a discount in the session
        session_params['line_items'][0]['price_data']['unit_amount'] = int(
            session_params['line_items'][0]['price_data']['unit_amount'] * 
            (1 - order.discount.percent_off / 100)
        )
    
    # Add tax if available
    if order.tax and order.tax.stripe_tax_rate_id:
        for item in session_params['line_items']:
            item['tax_rates'] = [order.tax.stripe_tax_rate_id]
    
    session = stripe.checkout.Session.create(**session_params)
    return session


def buy_item(request, id):
    """GET /buy/{id} - Returns Stripe Session ID for an item"""
    item = get_object_or_404(Item, id=id)
    session = create_checkout_session_for_item(item)
    return JsonResponse({'sessionId': session.id})


def item_detail(request, id):
    """GET /item/{id} - Returns HTML page with item info and Buy button"""
    item = get_object_or_404(Item, id=id)
    publishable_key = get_stripe_publishable_key_for_currency(item.currency)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <title>Buy {item.name}</title>
        <script src="https://js.stripe.com/v3/"></script>
      </head>
      <body>
        <h1>{item.name}</h1>
        <p>{item.description}</p>
        <p><strong>Price: {item.price} {item.currency.upper()}</strong></p>
        <button id="buy-button">Buy</button>
        <script type="text/javascript">
          var stripe = Stripe('{publishable_key}');
          var buyButton = document.getElementById('buy-button');
          buyButton.addEventListener('click', function() {{
            fetch('/buy/{item.id}', {{method: 'GET'}})
            .then(response => response.json())
            .then(data => stripe.redirectToCheckout({{ sessionId: data.sessionId }}))
            .catch(error => console.error('Error:', error));
          }});
        </script>
      </body>
    </html>
    """
    return HttpResponse(html_content)


def buy_order(request, id):
    """GET /buy/order/{id} - Returns Stripe Session ID for an order"""
    order = get_object_or_404(Order, id=id)
    session = create_checkout_session_for_order(order)
    return JsonResponse({'sessionId': session.id})


def order_detail(request, id):
    """GET /item/order/{id} - Returns HTML page with order info and Buy button"""
    order = get_object_or_404(Order, id=id)
    publishable_key = get_stripe_publishable_key_for_currency(order.currency)
    
    items_html = '<ul>'
    for item in order.items.all():
        items_html += f'<li>{item.name} - {item.price} {item.currency.upper()}</li>'
    items_html += '</ul>'
    
    discount_info = f'<p>Discount: {order.discount.name} ({order.discount.percent_off}%)</p>' if order.discount else ''
    tax_info = f'<p>Tax: {order.tax.name} ({order.tax.percentage}%)</p>' if order.tax else ''
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <title>Order #{order.id}</title>
        <script src="https://js.stripe.com/v3/"></script>
      </head>
      <body>
        <h1>Order #{order.id}</h1>
        <h2>Items:</h2>
        {items_html}
        {discount_info}
        {tax_info}
        <p><strong>Total: {order.total_price} {order.currency.upper()}</strong></p>
        <button id="buy-button">Buy</button>
        <script type="text/javascript">
          var stripe = Stripe('{publishable_key}');
          var buyButton = document.getElementById('buy-button');
          buyButton.addEventListener('click', function() {{
            fetch('/buy/order/{order.id}', {{method: 'GET'}})
            .then(response => response.json())
            .then(data => stripe.redirectToCheckout({{ sessionId: data.sessionId }}))
            .catch(error => console.error('Error:', error));
          }});
        </script>
      </body>
    </html>
    """
    return HttpResponse(html_content)


def success(request):
    """Success page after payment"""
    return HttpResponse('<h1>Payment successful!</h1><a href="/">Go back</a>')


def cancel(request):
    """Cancel page if payment is cancelled"""
    return HttpResponse('<h1>Payment cancelled</h1><a href="/">Go back</a>')

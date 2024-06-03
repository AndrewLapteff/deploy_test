const url = '/update_item/'
const buttons = document.querySelectorAll('.update-cart ')

buttons.forEach((button) => {
  button.addEventListener('click', function () {
    const productId = this.dataset.product
    const action = this.dataset.action

    if (user === 'AnonymousUser') {
      addCookieItem(productId, action)
    } else {
      updateUserOrder(productId, action)
    }
  })
})

function updateUserOrder(productId, action) {
  console.log('User is authenticated, sending data...')

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ productId, action }),
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      console.log('data:', data)
      location.reload()
    })
}

function addCookieItem(productId, action) {
  if (action === 'add') {
    if (cart[productId] === undefined) {
      cart[productId] = { quantity: 1 }
    } else {
      cart[productId]['quantity'] += 1
    }
  }

  if (action === 'remove') {
    cart[productId]['quantity'] -= 1

    if (cart[productId]['quantity'] <= 0) {
      console.log('Item should be deleted')
      delete cart[productId]
    }
  }

  document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
  location.reload()
}

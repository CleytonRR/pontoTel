loading = document.getElementById('loading').classList
result = document.getElementById('price_action')

spanResult = document.createElement('span')
function getBovespa() {
    axios.get('http://127.0.0.1:5000/v1/bovespa/')
    .then(function (response) {
        price = document.getElementById('price')
        price.innerText = formatValue(response.data.BOVESPA)
    })
    .catch(function (error) {
        price = document.getElementById('price')
        price.innerText = 'Erro ao carregar tente novamente em um minuto'
    })
}

function getPriceByName(nome) {
    spanResult.innerText = ''
    axios.get(`http://127.0.0.1:5000/v1/busca/${nome}/`)
        .then(function (response) {
            resultPrice = document.createTextNode(`${nome}: ${response.data.value}`)
            spanResult.appendChild(resultPrice)
            result.appendChild(spanResult)
        })
        .catch(function(error) {
            result = document.createTextNode('Erro ao carregar tente novamente em um minuto')
            spanResult.appendChild(result)
            result.appendChild(spanResult)
        })
        .then(function() {
            result.classList.remove('loading')
            loading.add('loading')
        })
}

function formatValue(price) {
    price = Number(price)
    return price.toLocaleString('pt-BR', { maximumSignificantDigits: 7 });
}

window.onload = getBovespa

imgs = document.querySelectorAll(".carousel a")
for(var i = 0; i < imgs.length; i++) {
    imgs[i].addEventListener("click", function(e) {
        loading.remove('loading')
        console.log(this.getElementsByTagName('span')[0].innerText)
        getPriceByName(this.getElementsByTagName('span')[0].innerText)
    })
}
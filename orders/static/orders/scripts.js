var modal = document.getElementById("customiseModel")
span = document.querySelector('.close')
function cart(type,toppings,quantity,price,id) {
  var content = document.getElementById('content')
    modal.style.display = "block";
    if (quantity == 0 || quantity.length == 0){
      quantity = 1
    }
    if(toppings != 0){
      var total = Number(price) * Number(quantity)
      content.innerHTML = `
      <font color="red"><span>Max of ${toppings} toppings</span></font><br><br>
      <form id="toppings" name="toppings" action="{% url 'setpizza' %}" method="POST">
        {% csrf_token %}
        <input type="number" value="${id}" name="id" hidden>
        <input type="text" value="${type}" name="name" hidden>
        <b>Quantity :</b> <input type="number" value="${quantity}" name="quantity" disabled><br>
        <b>Total Price($): </b> <input type="text" value="${total.toFixed(2)}" name="price" disabled><br>
      {% for topping in toppings %}
        <label>{{topping.name}}</label>
        <input type="checkbox" name="check" class='check' value="{{topping.name}}">&nbsp;
      {% endfor %}
      <input type="submit" class="btn btn-info" value="Add to cart">
      </form>
      <br><br>
      `
      checkboxlimit(document.forms.toppings.check, toppings)
    } else {
      var total = Number(price) * Number(quantity)
      content.innerHTML = `
      <form action="{% url 'setpizza' %}" method="POST">
        {% csrf_token %}
        <input type="number" value="${id}" name="id" hidden>
        <input type="text" value="${type}" name="name" hidden>
      <b>Quantity :</b> <input type="number" value="${quantity}" name="quantity" disabled><br>
      <b>Total Price($): </b> <input type="text" value="${total.toFixed(2)}" name="price" disabled><br>
      <br><br>
      <input type="submit" class="btn btn-info" value="Add to cart">
      </form>
      `
    }
}

function checkboxlimit(checkgroup, limit){
  var checkgroup=checkgroup
  var limit=limit
  for (var i=0; i<checkgroup.length; i++){
    checkgroup[i].onclick=function(){
    var checkedcount=0
    for (var i=0; i<checkgroup.length; i++)
      checkedcount+=(checkgroup[i].checked)? 1 : 0
    if (checkedcount>limit){
      this.checked=false
      }
    }
  }
}

span.onclick = function () {
  modal.style.display = "none";
}

window.onlick = function (event) {
  if (event.target == modal){
    modal.style.display = "none";
  }
}

function subway_cart(type,quantity,price,id) {
  var content = document.getElementById('content')
  modal.style.display = "block";
    if (quantity == 0 || quantity.length == 0){
      quantity = 1
    }
      var total = Number(price) * Number(quantity)
      content.innerHTML = `
      <form action="{% url 'setpizza' %}" method="POST">
        {% csrf_token %}
        <input type="number" value="${id}" name="id" hidden>
        <input type="text" value="${type}" name="name" hidden>
        <b>Quantity :</b> <input type="number" value="${quantity}" name="quantity" id="quantity "disabled><br>
        <b>Total Price($): </b> <input type="number" value="${total.toFixed(2)}" name="price" disabled><br><br>
        Each extra item is $0.50<br><br>
        <div id="extras">
          {% for extra in extras %}
          <label>{{extra.name}}</label>
          <input type="checkbox" name="{{extra.name}}" class='check' value="{{extra.name}}")">&nbsp;
          {% endfor %}
        </div>
      <br>
      <input type="submit" class="btn btn-info" value="Add to cart">
      </form>
      <br><br>
      `
      function attachCheckboxHandlers() {
    // get reference to element containing toppings checkboxes
    var el = document.getElementById('extras');

    // get reference to input elements in toppings container element
    var tops = el.getElementsByTagName('input');
    
    // assign updateTotal function to onclick property of each checkbox
    for (var i=0, len=tops.length; i<len; i++) {
        if ( tops[i].type === 'checkbox' ) {
            tops[i].onclick = updateTotal;
        }
    }
}
    
// called onclick of toppings checkboxes
function updateTotal(e) {
    // 'this' is reference to checkbox clicked on
    var form = this.form;
    
    // get current value in total text box, using parseFloat since it is a string
    var val = parseFloat( form.elements['price'].value );
    
    // if check box is checked, add its value to val, otherwise subtract it
    if ( this.checked ) {
        val += 0.50;
    } else {
        val -= 0.50;
    }
    
    // format val with correct number of decimal places
    // and use it to update value of total text box
    form.elements['price'].value = formatDecimal(val);
}
    
// format val to n number of decimal places
// modified version of Danny Goodman's (JS Bible)
function formatDecimal(val, n) {
    n = n || 2;
    var str = "" + Math.round ( parseFloat(val) * Math.pow(10, n) );
    while (str.length <= n) {
        str = "0" + str;
    }
    var pt = str.length - n;
    return str.slice(0,pt) + "." + str.slice(pt);
}

// in script segment below form
attachCheckboxHandlers();
}
    // call onload or in script segment below form

function pastas_cart() {
  
}

function platters_cart() {
  
}
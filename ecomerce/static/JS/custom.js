$(document).ready(function () {
  /* TODO arregladas funciones de decremento e incremento */
  $(".increment-btn").click(function (e) {
   
    e.preventDefault();
    let valor_inicial = $(this)
      .closest("#producto_data")
      .find("#qty_input")
      .val();
    let value = parseInt(valor_inicial, 10);
    value = isNaN(value) ? 0 : value;
    let stock_total = Number(
      $(this).closest("#producto_data").find("#stock-producto").val()
    );
    stock_total = stock_total > 0 ? stock_total : 10
    console.log(valor_inicial)
    if (value < stock_total) {
      value++;
      $(this).closest("#producto_data").find("#qty_input").val(value);
    }
  });
  $(".decrement-btn").click(function (e) {
    e.preventDefault();
    let valor_inicial = $(this)
      .closest("#producto_data")
      .find("#qty_input")
      .val();
    let value = parseInt(valor_inicial, 10);
    value = isNaN(value) ? 0 : value;

    if (value > 1) {
      value--;
      $(this).closest("#producto_data").find("#qty_input").val(value);
    }
  });
  /* End TODO */
  /*  */
  /* Agregar al carrito y a la lista de deseos */
  $("#add-to-cart").click(function (e) {
    e.preventDefault();
    let prod_id = $(this).closest("#producto_data").find("#producto_id").val();
    let prod_qty = $(this).closest("#producto_data").find("#qty_input").val();
    let token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      method: "POST",
      url: "/agregar-al-carrito",
      data: {
        producto_id: prod_id,
        producto_cantidad: prod_qty,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
      },
    });
  });
  $("#add-to-wish").click(function (e) {
    e.preventDefault();

    let prod_id = $(this).closest(".product_data").find("#producto_id").val();
    let token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      method: "POST",
      url: "/agregar-a-la-lista",
      data: {
        producto_id: prod_id,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
      },
    });
  });
  /* End agregar a al carrito y lista */
  $(".changeQuantity").click(function (e) {
    e.preventDefault();
    var prod_id = $(this).closest("#producto_data").find("#producto_id").val();
    var prod_qty = $(this).closest("#producto_data").find("#qty_input").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      method: "POST",
      url: "/actualizar-carrito",
      data: {
        producto_id: prod_id,
        producto_cantidad: prod_qty,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
      },
    });
  });
  $(document).on("click", "#borrar-item", function (e) {
    e.preventDefault();
    let prod_id = $(this).closest("#producto_data").find("#producto-id").val();
    let token = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      method: "POST",
      url: "/borrar-del-carrito",
      data: {
        producto_id: prod_id,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
        $("#cart-data").load(location.href + " #cart-data");
      },
    });
  });
  $(document).on("click", "#delete-wishlist", function (e) {
    e.preventDefault();
    let prod_id = $(this).closest("#producto_data").find("#producto_id").val();
    let token = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      method: "POST",
      url: "/borrar-de-favoritos",
      data: {
        producto_id: prod_id,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
        $("#wish_data").load(location.href + " #wish_data");
      },
    });
  });
});

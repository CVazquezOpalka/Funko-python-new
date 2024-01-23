$(document).ready(function () {
  $(".increment-btn").click(function (e) {
    e.preventDefault();
    let valor_inicial = $(this)
      .closest(".product_data")
      .find("#qty_input")
      .val();
    let value = parseInt(valor_inicial, 10);
    value = isNaN(value) ? 0 : value;
    let stock_total = Number(
      $(this).closest(".product_data").find("#stock-producto").val()
    );
    if (value < stock_total) {
      value++;
      $(this).closest(".product_data").find("#qty_input").val(value);
    }
  });
  $(".decrement-btn").click(function (e) {
    e.preventDefault();
    let valor_inicial = $(this)
      .closest(".product_data")
      .find("#qty_input")
      .val();
    let value = parseInt(valor_inicial, 10);
    value = isNaN(value) ? 0 : value;
    if (value > 1) {
      value--;
      $(this).closest(".product_data").find("#qty_input").val(value);
    }
  });
  $("#add-to-cart").click(function (e) {
    e.preventDefault();
    let prod_id = $(this).closest(".product_data").find("#producto_id").val();
    let prod_qty = $(this).closest(".product_data").find("#qty_input").val();
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
   $("#add-to-cart").click(function (e) {
     e.preventDefault();
     let prod_id = $(this).closest(".product_data").find("#producto_id").val();
     let prod_qty = $(this).closest(".product_data").find("#qty_input").val();
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
});

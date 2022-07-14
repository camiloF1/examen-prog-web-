class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar(self, producto):
        idProducto = str(producto.idProducto)
        if idProducto not in self.carrito.keys():
            self.carrito[idProducto]={
                "producto_id": producto.idProducto,
                "nombre": producto.nombreProducto,
                "acumulado": producto.precio,
                "cantidad": 1,
            }
        else:
            self.carrito[idProducto]["cantidad"] += 1
            self.carrito[idProducto]["acumulado"] += producto.precio
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        idProducto = str(producto.idProducto)
        if idProducto in self.carrito:
            del self.carrito[idProducto]
            self.guardar_carrito()

    def restar(self, producto):
        idProducto = str(producto.idProducto)
        if idProducto in self.carrito.keys():
            self.carrito[idProducto]["cantidad"] -= 1
            self.carrito[idProducto]["acumulado"] -= producto.precio
            if self.carrito[idProducto]["cantidad"] <= 0: self.eliminar(producto)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
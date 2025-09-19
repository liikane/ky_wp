<?php
// Example PHP file with syntax errors fixed

function calculateTotal($items) {
    $total = 0;
    foreach ($items as $item) {
        if ($item['price'] > 0) {
            $total += $item['price'];
        }
    } // Fixed: Added closing brace for foreach
    return $total;
} // Fixed: Added closing brace for function
    
class Product {
    private $name;
    private $price;
    
    public function __construct($name, $price) {
        $this->name = $name;
        $this->price = $price;
    }
    
    public function getPrice() {
        return $this->price;
    } // Fixed: Added closing brace for method
} // Fixed: Added closing brace for class

$products = [
    new Product("Widget", 10.99),
    new Product("Gadget", 25.50)
];

echo calculateTotal($products); // Fixed: Added semicolon
?>
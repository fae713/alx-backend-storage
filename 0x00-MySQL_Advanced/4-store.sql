--  a SQL script that creates a trigger that decreases the quantity of an item after adding a new order.

-- Quantity in the table items can be negative.

DELIMITER $$

CREATE TRIGGER after_order_insert
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    DECLARE item_quantity INT;
    
    SELECT quantity INTO item_quantity FROM items WHERE name = NEW.item_name;
    
    UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW.item_name;
END$$

DELIMITER ;

use pipeline1;
CREATE TABLE users (
  user_id INT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(150),
  age INT,
  address VARCHAR(255)
);

CREATE TABLE products (
  product_id INT PRIMARY KEY,
  name VARCHAR(150),
  category VARCHAR(100),
  price DECIMAL(10,2),
  stock INT
);

CREATE TABLE orders (
  order_id INT PRIMARY KEY,
  user_id INT,
  product_id INT,
  quantity INT,
  order_date DATE,
  total_amount DECIMAL(10,2),
  price DECIMAL(10,2),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE payments (
  payment_id INT PRIMARY KEY,
  order_id INT,
  amount DECIMAL(10,2),
  payment_date DATE,
  status VARCHAR(50),
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

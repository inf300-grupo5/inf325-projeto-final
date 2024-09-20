CREATE TABLE payment_methods (
	id uuid NOT NULL,
	"type" varchar(50) NULL,
	"name" varchar(255) NULL,
	CONSTRAINT payment_methods_id PRIMARY KEY (id)
);

CREATE TABLE products (
	id uuid NOT NULL,
	title varchar(255) NULL,
	publisher varchar(255) NULL,
	parental_guidance varchar(50) NULL,
	release_date date NULL,
	updated_at date NULL,
	price int8 NULL,
	genre varchar(100) NULL,
	platform varchar(100) NULL,
	"system" varchar(100) NULL,
	discount float8 NULL,
	CONSTRAINT products_id PRIMARY KEY (id)
);

CREATE TABLE users (
	id uuid NOT NULL,
	first_name varchar(255) NULL,
	last_name varchar(255) NULL,
	username varchar(255) NULL,
	gender varchar(50) NULL,
	cpf varchar(14) NULL,
	birth_date date NULL,
	CONSTRAINT users_id PRIMARY KEY (id)
);

CREATE TABLE orders (
	id uuid NOT NULL,
	code varchar(100) NULL,
	user_id uuid NULL,
	created_at date NULL,
	updated_at date NULL,
	status varchar(50) NULL,
	coupon_code varchar(50) NULL,
	payment_method_id uuid NULL,
	CONSTRAINT orders_id PRIMARY KEY (id),
	CONSTRAINT payment_method_id FOREIGN KEY (payment_method) REFERENCES payment_methods(id),
	CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES users(id)
);


CREATE TABLE orders_items (
	id uuid NOT NULL,
	order_id uuid NULL,
	product_id uuid NULL,
	price int8 NULL,
	discount float8 NULL,
	CONSTRAINT items_id PRIMARY KEY (id),
	CONSTRAINT order_id FOREIGN KEY (order_id) REFERENCES orders(id),
	CONSTRAINT product_id FOREIGN KEY (product_id) REFERENCES products(id)
);

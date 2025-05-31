-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 31, 2025 at 07:28 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `coffeeshopv2`
--

-- --------------------------------------------------------

--
-- Table structure for table `address`
--

CREATE TABLE `address` (
  `AddressID` int(11) NOT NULL,
  `CustomerID` int(11) DEFAULT NULL,
  `Province` varchar(100) DEFAULT NULL,
  `District` varchar(100) DEFAULT NULL,
  `Ward` varchar(100) DEFAULT NULL,
  `Detail` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `address`
--

INSERT INTO `address` (`AddressID`, `CustomerID`, `Province`, `District`, `Ward`, `Detail`) VALUES
(12, 2, '2', '35', '1258', 'q'),
(13, 2, '22', '203', '7024', 'q'),
(14, 2, '22', '203', '7027', 'q'),
(15, 2, '22', '203', '7000', 'q'),
(16, 2, '22', '203', '7027', 'q'),
(17, 2, '22', '203', '7024', 'q'),
(18, 2, '22', '207', '7198', 'q'),
(19, 2, '22', '207', '7192', 'q'),
(20, 2, '22', '207', '7192', 'q'),
(21, 2, '22', '207', '7195', 'q');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `CartID` int(11) NOT NULL,
  `CustomerID` int(11) DEFAULT NULL,
  `ProductID` int(11) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`CartID`, `CustomerID`, `ProductID`, `Quantity`) VALUES
(30, 2, 9, 1);

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `CategoryID` int(11) NOT NULL,
  `Name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`CategoryID`, `Name`) VALUES
(1, 'Whole Bean'),
(2, 'Ground Coffee'),
(3, 'Coffee Pods'),
(4, 'Accessories');

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `ContactID` int(11) NOT NULL,
  `CustomerID` int(11) DEFAULT NULL,
  `ContactMethod` enum('email','phone','chat') DEFAULT NULL,
  `ContactDetails` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `CustomerID` int(11) NOT NULL,
  `Firstname` varchar(100) DEFAULT NULL,
  `Lastname` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Username` varchar(50) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `PhoneNum` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`CustomerID`, `Firstname`, `Lastname`, `Email`, `Username`, `Password`, `PhoneNum`) VALUES
(1, 'John', 'Doe', 'john.doe@example.com', 'johndoe', '123456', '0123456789'),
(2, 'Detina', 'Tran', '23070589@vnu.edu.vn', 'duong', '$2y$10$vfiBF.WF5tqAnhGqj1EK0.nsxDskpdmS3Qx1SdFwX7R52vgFdMIw.', '0327459598');

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `FeedbackID` int(11) NOT NULL,
  `CustomerID` int(11) DEFAULT NULL,
  `OrderID` int(11) DEFAULT NULL,
  `Rating` int(11) DEFAULT NULL,
  `Comment` varchar(255) DEFAULT NULL,
  `FeedbackDate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

CREATE TABLE `order` (
  `OrderID` int(11) NOT NULL,
  `CustomerID` int(11) DEFAULT NULL,
  `OrderDate` date DEFAULT NULL,
  `TotalPrice` decimal(10,2) DEFAULT NULL,
  `Status` enum('pending','confirmed','shipped','delivered','cancelled','awaiting payment') DEFAULT NULL,
  `PhoneNum` varchar(20) DEFAULT NULL,
  `AddressID` int(11) DEFAULT NULL,
  `PaymentMethod` varchar(20) DEFAULT 'cod',
  `PaymentID` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order`
--

INSERT INTO `order` (`OrderID`, `CustomerID`, `OrderDate`, `TotalPrice`, `Status`, `PhoneNum`, `AddressID`, `PaymentMethod`, `PaymentID`) VALUES
(1, 2, NULL, 66.98, 'pending', '0327459598', 12, 'cod', NULL),
(2, 2, NULL, 17.99, 'pending', '0327459598', 13, 'cod', NULL),
(3, 2, NULL, 35.98, 'pending', '0327459598', 14, 'cod', NULL),
(4, 2, NULL, 35.98, 'pending', '0327459598', 15, 'cod', NULL),
(5, 2, NULL, 15.00, 'pending', '0327459598', 16, 'cod', NULL),
(6, 2, NULL, 29.50, 'pending', '0327459598', 17, 'cod', NULL),
(7, 2, NULL, 17.99, 'pending', '0327459598', 18, 'cod', NULL),
(8, 2, NULL, 17.99, 'pending', '0327459598', 19, 'cod', NULL),
(9, 2, NULL, 35.98, 'pending', '0327459598', 20, 'cod', NULL),
(10, 2, NULL, 17.99, 'pending', '0327459598', 21, 'cod', NULL),
(11, 2, NULL, 29.50, 'pending', '0327459598', 12, 'cod', NULL),
(12, 2, '2025-05-29', 17.99, 'pending', '0327459598', 12, 'cod', NULL),
(13, 2, '2025-05-31', 17.99, 'awaiting payment', '0327459598', 12, 'vnpay', NULL),
(14, 2, '2025-05-31', 17.99, 'awaiting payment', '0327459598', 12, 'vnpay', NULL),
(15, 2, '2025-05-31', 17.99, 'awaiting payment', '0327459598', 12, 'vnpay', NULL),
(16, 2, '2025-05-31', 35.98, 'awaiting payment', '0327459598', 12, 'vnpay', NULL),
(17, 2, '2025-05-31', 17.99, 'awaiting payment', '0327459598', 12, 'vnpay', NULL),
(18, 2, '2025-05-31', 17.99, 'awaiting payment', '0327459598', 12, 'vnpay', NULL),
(19, 2, '2025-05-31', 17.99, 'awaiting payment', '0327459598', 12, 'vnpay', NULL),
(20, 2, '2025-05-31', 17.99, 'awaiting payment', '0327459598', 12, 'vnpay', NULL),
(21, 2, '2025-05-31', 17.99, 'pending', '0327459598', 12, 'cod', NULL),
(22, 2, '2025-05-31', 17.99, 'awaiting payment', '0327459598', 12, 'vnpay', NULL),
(23, 2, '2025-05-31', 17.99, 'awaiting payment', '0327459598', 12, 'vnpay', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `orderdetail`
--

CREATE TABLE `orderdetail` (
  `OrderDetailID` int(11) NOT NULL,
  `OrderID` int(11) DEFAULT NULL,
  `ProductID` int(11) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `UnitPrice` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orderdetail`
--

INSERT INTO `orderdetail` (`OrderDetailID`, `OrderID`, `ProductID`, `Quantity`, `UnitPrice`) VALUES
(1, 1, 9, 2, 17.99),
(2, 1, 2, 1, 15.50),
(3, 1, 6, 1, 15.50),
(4, 2, 9, 1, 17.99),
(5, 3, 9, 2, 17.99),
(6, 4, 9, 2, 17.99),
(7, 5, 20, 1, 15.00),
(8, 6, 18, 1, 29.50),
(9, 7, 9, 1, 17.99),
(10, 8, 9, 1, 17.99),
(11, 9, 9, 2, 17.99),
(12, 10, 9, 1, 17.99),
(13, 11, 18, 1, 29.50),
(14, 12, 9, 1, 17.99),
(15, 13, 9, 1, 17.99),
(16, 14, 9, 1, 17.99),
(17, 15, 9, 1, 17.99),
(18, 16, 9, 2, 17.99),
(19, 17, 9, 1, 17.99),
(20, 18, 9, 1, 17.99),
(21, 19, 9, 1, 17.99),
(22, 20, 9, 1, 17.99),
(23, 21, 9, 1, 17.99),
(24, 22, 9, 1, 17.99),
(25, 23, 9, 1, 17.99);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `ProductID` int(11) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `CategoryID` int(11) DEFAULT NULL,
  `StockQuantity` int(11) DEFAULT NULL,
  `ImageURL` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`ProductID`, `Name`, `Description`, `Price`, `CategoryID`, `StockQuantity`, `ImageURL`) VALUES
(1, 'Ethiopian Yirgacheffe', 'Bright, citrusy, and floral notes. Whole bean.', 19.99, 1, 50, 'images/ethiopian_yirgacheffe.jpg'),
(2, 'Colombian Supremo', 'Smooth, nutty, and chocolatey. Medium roast, ground.', 15.50, 2, 29, 'images/colombian_supremo.jpg'),
(3, 'Dark Roast Espresso Pods', 'Intense and rich espresso pods. Pack of 20.', 12.00, 3, 100, 'images/espresso_pods.jpg'),
(4, 'French Press', 'Classic 3-cup French press coffee maker.', 25.00, 4, 15, 'images/french_press.jpg'),
(5, 'Ethiopian Yirgacheffe', 'Bright, citrusy, and floral notes. Whole bean.', 19.99, 1, 50, 'images/ethiopian_yirgacheffe.jpg'),
(6, 'Colombian Supremo', 'Smooth, nutty, and chocolatey. Medium roast, ground.', 15.50, 2, 29, 'images/colombian_supremo.jpg'),
(7, 'Dark Roast Espresso Pods', 'Intense and rich espresso pods. Pack of 20.', 12.00, 3, 100, 'images/espresso_pods.jpg'),
(8, 'French Press', 'Classic 3-cup French press coffee maker.', 25.00, 4, 15, 'images/french_press.jpg'),
(9, 'Brazilian Santos', 'A smooth, low-acidity coffee with nutty and sweet chocolate notes. Excellent for espresso. Whole bean.', 17.99, 1, 35, 'images/brazilian_santos.jpg'),
(10, 'Kenyan AA Washed', 'Bright acidity, full body, with notes of blackcurrant and citrus. Whole bean.', 21.50, 1, 40, 'images/kenyan_aa.jpg'),
(11, 'Sumatra Mandheling', 'Earthy, complex, and full-bodied with a syrupy richness. Dark roast, ground.', 18.75, 2, 35, 'images/sumatra_mandheling.jpg'),
(12, 'Costa Rican Tarrazu', 'Clean, crisp, with bright citrus notes and a hint of chocolate. Medium roast, ground.', 16.90, 2, 55, 'images/costa_rican_tarrazu.jpg'),
(13, 'Decaf Colombian Excelso', 'Full-flavored decaf using Swiss Water Process. Notes of caramel and nuts. Whole bean.', 19.25, 1, 25, 'images/decaf_colombian.jpg'),
(14, 'Hazelnut Flavored Coffee', 'Smooth Arabica beans infused with rich hazelnut flavor. Ground.', 14.50, 2, 70, 'images/hazelnut_flavored.jpg'),
(15, 'Variety Pack Coffee Pods', 'A mix of our most popular coffee pods. 30 count.', 22.00, 3, 80, 'images/variety_pods.jpg'),
(16, 'Reusable Coffee Filter', 'Eco-friendly stainless steel mesh filter for pour-over or drip machines.', 12.99, 4, 45, 'images/reusable_filter.jpg'),
(17, 'Gooseneck Kettle', 'Stainless steel gooseneck kettle for precise pour-over brewing. 1L capacity.', 39.99, 4, 20, 'images/gooseneck_kettle.jpg'),
(18, 'Coffee Grinder - Manual', 'Burr grinder for a consistent grind. Portable and perfect for travel.', 29.50, 4, 28, 'images/manual_grinder.jpg'),
(19, 'Espresso Blend - Dark Knight', 'Our signature dark roast espresso blend. Rich, intense, with notes of dark chocolate and smoke. Whole bean.', 20.50, 1, 50, 'images/espresso_dark_knight.jpg'),
(20, 'Breakfast Blend - Morning Light', 'A bright and cheerful medium roast to start your day. Ground.', 15.00, 2, 64, 'images/breakfast_blend.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `returnpolicy`
--

CREATE TABLE `returnpolicy` (
  `ReturnPolicyID` int(11) NOT NULL,
  `CustomerID` int(11) DEFAULT NULL,
  `ReturnDate` date DEFAULT NULL,
  `Reason` varchar(255) DEFAULT NULL,
  `Status` enum('pending','approved','rejected') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `support`
--

CREATE TABLE `support` (
  `SupportID` int(11) NOT NULL,
  `CustomerID` int(11) DEFAULT NULL,
  `RequestType` enum('technical','billing','general') DEFAULT NULL,
  `SupportDate` date DEFAULT NULL,
  `IssueDescription` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `address`
--
ALTER TABLE `address`
  ADD PRIMARY KEY (`AddressID`),
  ADD KEY `CustomerID` (`CustomerID`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`CartID`),
  ADD KEY `CustomerID` (`CustomerID`),
  ADD KEY `ProductID` (`ProductID`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`CategoryID`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`ContactID`),
  ADD KEY `CustomerID` (`CustomerID`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`CustomerID`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`FeedbackID`),
  ADD KEY `CustomerID` (`CustomerID`),
  ADD KEY `OrderID` (`OrderID`);

--
-- Indexes for table `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`OrderID`),
  ADD KEY `CustomerID` (`CustomerID`),
  ADD KEY `fk_AddressID` (`AddressID`);

--
-- Indexes for table `orderdetail`
--
ALTER TABLE `orderdetail`
  ADD PRIMARY KEY (`OrderDetailID`),
  ADD KEY `OrderID` (`OrderID`),
  ADD KEY `ProductID` (`ProductID`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`ProductID`),
  ADD KEY `CategoryID` (`CategoryID`);

--
-- Indexes for table `returnpolicy`
--
ALTER TABLE `returnpolicy`
  ADD PRIMARY KEY (`ReturnPolicyID`),
  ADD KEY `CustomerID` (`CustomerID`);

--
-- Indexes for table `support`
--
ALTER TABLE `support`
  ADD PRIMARY KEY (`SupportID`),
  ADD KEY `CustomerID` (`CustomerID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `address`
--
ALTER TABLE `address`
  MODIFY `AddressID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `CartID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `CategoryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `ContactID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `CustomerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `FeedbackID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `order`
--
ALTER TABLE `order`
  MODIFY `OrderID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `orderdetail`
--
ALTER TABLE `orderdetail`
  MODIFY `OrderDetailID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `ProductID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `returnpolicy`
--
ALTER TABLE `returnpolicy`
  MODIFY `ReturnPolicyID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `support`
--
ALTER TABLE `support`
  MODIFY `SupportID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `address`
--
ALTER TABLE `address`
  ADD CONSTRAINT `address_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`);

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`),
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`);

--
-- Constraints for table `contact`
--
ALTER TABLE `contact`
  ADD CONSTRAINT `contact_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`);

--
-- Constraints for table `feedback`
--
ALTER TABLE `feedback`
  ADD CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`),
  ADD CONSTRAINT `feedback_ibfk_2` FOREIGN KEY (`OrderID`) REFERENCES `order` (`OrderID`);

--
-- Constraints for table `order`
--
ALTER TABLE `order`
  ADD CONSTRAINT `fk_AddressID` FOREIGN KEY (`AddressID`) REFERENCES `address` (`AddressID`),
  ADD CONSTRAINT `order_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`);

--
-- Constraints for table `orderdetail`
--
ALTER TABLE `orderdetail`
  ADD CONSTRAINT `orderdetail_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `order` (`OrderID`),
  ADD CONSTRAINT `orderdetail_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`);

--
-- Constraints for table `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `product_ibfk_1` FOREIGN KEY (`CategoryID`) REFERENCES `category` (`CategoryID`);

--
-- Constraints for table `returnpolicy`
--
ALTER TABLE `returnpolicy`
  ADD CONSTRAINT `returnpolicy_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`);

--
-- Constraints for table `support`
--
ALTER TABLE `support`
  ADD CONSTRAINT `support_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

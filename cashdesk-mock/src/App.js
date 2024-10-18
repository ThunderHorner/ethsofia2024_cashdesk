import React, { useEffect, useState } from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { add } from 'date-fns';

function App() {
    // Mock data for products
    const products = [
        { barcodeId: '8434344012481', ProductName: 'Very nice thermos', Price: "10.00", RequiresWarranty: true, Delta: { years: 2 } },
        { barcodeId: '234567', ProductName: 'Product B', Price: "15.50" },
        { barcodeId: '345678', ProductName: 'Product C', Price: "7.25" },
    ];

    const [scannedProducts, setScannedProducts] = useState([]);
    const [barcodeInput, setBarcodeInput] = useState('');
    const [total, setTotal] = useState(0);
    const [serialNumberInput, setSerialNumberInput] = useState('');

    // Function to print receipt via Flask API
    const printReceipt = async () => {
        const receiptData = {
            orderNumber: Math.floor(Math.random() * 1000).toString(), // Mock order number
            items: scannedProducts,
            total: total.toFixed(2)
        };

        try {
            const response = await fetch('http://localhost:5555/print-receipt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(receiptData)
            });
            console.log(JSON.stringify(receiptData))
            if (response.ok) {
                setScannedProducts([]);
                setBarcodeInput('');
                setTotal(0);
                setSerialNumberInput('');
                // alert("Receipt printed successfully!");
            } else {
                alert("Failed to print receipt.");
            }
        } catch (error) {
            console.error("Error printing receipt:", error);
            alert("Error printing receipt.");
        }
    };
    useEffect(() => {
        const product = products.find(p => p.barcodeId === barcodeInput);
        if (product) {
            if (product.RequiresWarranty) {
                const serialNumber = '123123123';//prompt(`Please enter the serial number for ${product.ProductName}:`);
                if (serialNumber) {
                    product.SerialNumber = serialNumber;
                    const warrantyEndDate = add(new Date(), product.Delta);
                    product.WarrantyEndDate = warrantyEndDate.toISOString().split('T')[0];
                } else {
                    alert("Serial number is required for warranty products.");
                    return;
                }
            }
            setScannedProducts([...scannedProducts, product]);
            setTotal(total + parseFloat(product.Price));
            setBarcodeInput('');
        }
    }, [barcodeInput]);

    return (
        <div className="App container mt-5">
            <p className="h2">Demo CashDesk</p>

            <div className="mb-3">
                <input
                    type="text"
                    className="form-control"
                    placeholder="Enter barcode"
                    value={barcodeInput}
                    onChange={(e) => {
                        setBarcodeInput(e.target.value);
                    }}
                />
            </div>

            <table className="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">Product Name</th>
                        <th scope="col">Price</th>
                        <th scope="col">Serial Number</th>
                        <th scope="col">Warranty End Date</th>
                    </tr>
                </thead>
                <tbody>
                    {scannedProducts.map((product, index) => (
                        <tr key={index}>
                            <td>{product.ProductName}</td>
                            <td>{product.Price}</td>
                            <td>{product.RequiresWarranty ? product.SerialNumber : 'N/A'}</td>
                            <td>{product.RequiresWarranty ? product.WarrantyEndDate : 'N/A'}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <div className="mt-3">
                <p className="h5">Total: ${total.toFixed(2)}</p>
                <button className="btn btn-success" onClick={printReceipt}>Pay Now</button>
            </div>
        </div>
    );
}

export default App;

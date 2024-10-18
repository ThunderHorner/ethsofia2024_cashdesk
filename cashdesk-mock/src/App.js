import React, {useEffect, useState} from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
    // Mock data for products
    const products = [
        {barcodeId: '123456', ProductName: 'Product A', Price: 10.0},
        {barcodeId: '234567', ProductName: 'Product B', Price: 15.5},
        {barcodeId: '345678', ProductName: 'Product C', Price: 7.25},
    ];

    const [scannedProducts, setScannedProducts] = useState([]);
    const [barcodeInput, setBarcodeInput] = useState('');
    const [total, setTotal] = useState(0);

    useEffect(() => {
        const product = products.find(p => p.barcodeId === barcodeInput);
        if (product) {
            setScannedProducts([...scannedProducts, product]);
            setTotal(total + product.Price);
            setBarcodeInput('')
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
                        setBarcodeInput(e.target.value)
                    }}
                />
            </div>

            <table className="table table-striped">
                <thead>
                <tr>
                    <th scope="col">Product Name</th>
                    <th scope="col">Price</th>
                </tr>
                </thead>
                <tbody>
                {scannedProducts.map((product, index) => (
                    <tr key={index}>
                        <td>{product.ProductName}</td>
                        <td>{product.Price.toFixed(2)}</td>
                    </tr>
                ))}
                </tbody>
            </table>

            <div className="mt-3">
                <p className="h5">Total: ${total.toFixed(2)}</p>
                <button className="btn btn-success">Pay Now</button>
            </div>
        </div>
    );
}

export default App;

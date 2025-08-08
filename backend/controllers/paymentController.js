import crypto from 'crypto';

// Simulated config endpoint
const config = (req, res) =>
  res.send({
    razorpayKeyId: 'FAKE_KEY_ID',
    razorpayKeySecret: 'FAKE_KEY_SECRET'
  });

// Simulated order creation (always successful)
const order = async (req, res, next) => {
  try {
    const options = req.body;

    // Simulated order data (like Razorpay returns)
    const fakeOrder = {
      id: 'order_' + crypto.randomBytes(8).toString('hex'),
      amount: options.amount || 1000,
      currency: options.currency || 'INR',
      receipt: options.receipt || 'rcpt_' + Date.now(),
      status: 'created'
    };

    res.status(201).json(fakeOrder);
  } catch (error) {
    next(error);
  }
};

// Simulated validation (always successful)
const validate = (req, res) => {
  const { razorpay_order_id, razorpay_payment_id } = req.body;

  // No real signature check — just pretend it's valid
  res.status(201).json({
    id: razorpay_payment_id || 'pay_' + crypto.randomBytes(8).toString('hex'),
    status: 'success',
    message: 'Payment is successful (simulated)',
    updateTime: new Date().toLocaleTimeString()
  });
};

export { config, order, validate };
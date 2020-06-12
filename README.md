# thread-vs-asyncio
Comparing asyncio vs threads performances.

After reading [Async Python is not faster](http://calpaterson.com/async-python-is-not-faster.html),
I wanted to write my own experiment. I don't want to compare frameworks and will
only use the standard library. For simplicity, I won't write an HTTP server,
and will use a custom TCP protocol that will be close to what we have in real
life.

This protocol will allow 2 types of requests: the first will be a quick
one, let's say you're adding a product to your basket, the second one will be
longer and will call an external service, let's say you're computing the
shipping price of your basket.

Each client will first call `add_to_basket` then `get_shipping_price`. And I
will get the average response time those two requests.

Here are the different variables of this experiment:
- Number of concurrent connections (client side)
- Number of threads (server side)
- Latency of the external service

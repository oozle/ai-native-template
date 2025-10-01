export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname.startsWith('/api/')) {
      const receipt = request.headers.get('X-Usage-Receipt');
      if (!receipt) {
        return new Response(JSON.stringify({
          error: "Payment required",
          manifest: "https://oozle.github.io/ai-native-template/.well-known/agent-licensing.json"
        }), { status: 402, headers: { "content-type": "application/json" }});
      }
    }
    return fetch(request);
  }
};

/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        // Route all /api/* requests to the Python serverless function at /api/index.py
        destination: '/api/',
      },
    ]
  },
};

export default nextConfig;

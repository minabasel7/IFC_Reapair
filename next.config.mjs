/** @type {import('next').NextConfig} */
const nextConfig = {
  // If the backend is hosted separately, the API URL is handled by NEXT_PUBLIC_API_URL.
  // We can use a rewrite to avoid CORS issues if not set.
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL}/:path*` : '/api/:path*',
      },
    ]
  },
};

export default nextConfig;

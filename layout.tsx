export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{fontFamily:'system-ui, -apple-system, Segoe UI, Roboto, sans-serif', maxWidth: 860, margin: '0 auto', padding: 24}}>
        <header style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom: 24}}>
          <h1 style={{margin:0}}>Style Sage</h1>
          <a href="https://github.com/" target="_blank" rel="noreferrer" style={{textDecoration:'none'}}>GitHub</a>
        </header>
        {children}
        <footer style={{marginTop: 48, fontSize: 12, opacity: 0.7}}>
          <p>© {new Date().getFullYear()} Style Sage – MVP demo</p>
        </footer>
      </body>
    </html>
  );
}


// Simple authentication logic for demo purposes
// In a real app, this would connect to a backend service

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  return localStorage.getItem('sentinel-auth') === 'true';
};

// Login function
export const login = (username: string, password: string): Promise<boolean> => {
  return new Promise((resolve) => {
    // For demo, we'll accept "admin" with password "admin123"
    if (username === 'admin' && password === 'admin123') {
      localStorage.setItem('sentinel-auth', 'true');
      resolve(true);
    } else {
      resolve(false);
    }
  });
};

// Logout function
export const logout = (): void => {
  localStorage.removeItem('sentinel-auth');
  window.location.href = '/';
};

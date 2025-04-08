
import { apiAuth } from "./apiUtils";

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  return localStorage.getItem('sentinel-auth') === 'true';
};

// Login function
export const login = async (username: string, password: string): Promise<boolean> => {
  try {
    // Make sure we're actually reaching the FastAPI backend
    console.log("Attempting login with:", { username });
    
    const response = await apiAuth.login(username, password);
    console.log("Login response:", response);
    
    if (response && response.success) {
      localStorage.setItem('sentinel-auth', 'true');
      return true;
    }
    return false;
  } catch (error) {
    console.error("Login error:", error);
    return false;
  }
};

// Logout function
export const logout = (): void => {
  localStorage.removeItem('sentinel-auth');
  window.location.href = '/';
};

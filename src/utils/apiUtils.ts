
// API utilities for connecting to FastAPI backend

const API_URL = "http://localhost:8000/api";

// Generic fetch wrapper with error handling
async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_URL}${endpoint}`;
  
  console.log(`Making API request to: ${url}`);
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      // Important for CORS preflight to work correctly
      credentials: 'omit', 
      mode: 'cors',
    });

    console.log(`API response status: ${response.status}`);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`API error: ${response.status}`, errorText);
      throw new Error(errorText || `API error: ${response.status}`);
    }

    const data = await response.json();
    console.log("API response data:", data);
    return data;
  } catch (error) {
    console.error("API request failed:", error);
    throw error;
  }
}

// Authentication
export const apiAuth = {
  login: async (username: string, password: string) => {
    return fetchAPI<{ success: boolean; message?: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });
  },
};

// Transactions
export const apiTransactions = {
  getAll: async () => {
    return fetchAPI<any[]>("/transactions");
  },
};

// Feedback
export const apiFeedback = {
  submitTransactionFeedback: async (
    transactionId: string,
    isCorrect: boolean,
    feedback?: string
  ) => {
    return fetchAPI("/feedback/transaction", {
      method: "POST",
      body: JSON.stringify({
        transaction_id: transactionId,
        is_correct: isCorrect,
        feedback,
      }),
    });
  },
  submitSystemFeedback: async (category: string, details: string) => {
    return fetchAPI("/feedback/system", {
      method: "POST",
      body: JSON.stringify({
        category,
        details,
      }),
    });
  },
};

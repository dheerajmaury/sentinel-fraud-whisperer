
// API utilities for connecting to FastAPI backend

const API_URL = "http://localhost:8000/api";

// Generic fetch wrapper with error handling
async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_URL}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || `API error: ${response.status}`);
  }

  return response.json();
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

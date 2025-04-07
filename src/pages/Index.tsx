
import { useEffect } from "react";
import { Navigate } from "react-router-dom";
import { isAuthenticated } from "@/utils/authUtils";

const Index = () => {
  // Simply redirect to the appropriate page based on authentication status
  return <Navigate to={isAuthenticated() ? "/dashboard" : "/login"} replace />;
};

export default Index;


import { Button } from "@/components/ui/button";
import { logout } from "../utils/authUtils";
import { Shield, LogOut, Bell } from "lucide-react";

const Navbar = () => {
  return (
    <header className="border-b border-border sticky top-0 z-10 w-full bg-background/95 backdrop-blur">
      <div className="container flex h-16 items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <Shield className="h-6 w-6 text-primary" />
          <span className="text-xl font-bold">Sentinel</span>
        </div>
        
        <div className="flex items-center">
          <Button variant="ghost" size="icon" className="mr-2">
            <Bell className="h-5 w-5" />
          </Button>
          
          <Button 
            variant="secondary" 
            size="sm" 
            className="gap-2"
            onClick={() => logout()}
          >
            <LogOut className="h-4 w-4" />
            <span>Logout</span>
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Navbar;

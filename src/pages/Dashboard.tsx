
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import TransactionCard, { Transaction } from "../components/TransactionCard";
import ScoreGauge from "../components/ScoreGauge";
import FeedbackForm from "../components/FeedbackForm";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { Separator } from "../components/ui/separator";
import { Alert, AlertDescription, AlertTitle } from "../components/ui/alert";
import { isAuthenticated } from "../utils/authUtils";
import { toast } from "sonner";
import {
  FileDown,
  Filter,
  AlertTriangle,
  PieChart,
  BarChart3,
  Clock,
  Search,
  RefreshCw
} from "lucide-react";

// Demo data
const mockTransactions: Transaction[] = [
  {
    id: "T123456",
    timestamp: "2025-04-07T09:15:30",
    amount: 15000,
    accountNumber: "8765432109",
    transactionType: "wire",
    score: 0.85,
    reason: "Transaction T123456 was flagged because the amount of ₹15,000 exceeds typical daily averages by over 300% for this account. The transaction also occurred from an unusual IP address not previously associated with this account."
  },
  {
    id: "T123457",
    timestamp: "2025-04-07T10:23:45",
    amount: 5999,
    accountNumber: "7654321098",
    transactionType: "card",
    score: 0.62,
    reason: "Transaction T123457 was flagged due to unusual merchant category. This account typically performs transactions in retail and grocery, but this payment was made to a high-risk merchant category in a foreign jurisdiction."
  },
  {
    id: "T123458",
    timestamp: "2025-04-07T14:56:12",
    amount: 2500,
    accountNumber: "6543210987",
    transactionType: "online",
    score: 0.35,
    reason: "Transaction T123458 triggered a low-level alert due to being slightly outside normal spending patterns. The transaction amount is higher than average for this merchant type, but remains within reasonable bounds for the account history."
  },
  {
    id: "T123459",
    timestamp: "2025-04-06T18:34:22",
    amount: 12500,
    accountNumber: "5432109876",
    transactionType: "atm",
    score: 0.78,
    reason: "Transaction T123459 was flagged as potentially fraudulent because this ATM withdrawal occurred in a location over 500km from the account holder's typical transaction area. Additionally, there were 3 failed PIN attempts before this successful transaction."
  },
  {
    id: "T123460",
    timestamp: "2025-04-06T11:45:33",
    amount: 8750,
    accountNumber: "4321098765",
    transactionType: "pos",
    score: 0.52,
    reason: "Transaction T123460 raised moderate concern due to unusual timing. This transaction occurred at 11:45 PM, while the account holder typically makes purchases between 8 AM and 8 PM. The merchant category itself is not unusual for this customer."
  }
];

const Dashboard = () => {
  const [transactions, setTransactions] = useState<Transaction[]>(mockTransactions);
  const [feedbackVisible, setFeedbackVisible] = useState(false);
  const [filter, setFilter] = useState<"all" | "high" | "medium" | "low">("all");
  const [refreshing, setRefreshing] = useState(false);
  const navigate = useNavigate();

  // Check authentication
  useEffect(() => {
    if (!isAuthenticated()) {
      navigate("/login");
    }
  }, [navigate]);

  // Filter transactions based on risk level
  const filteredTransactions = transactions.filter(transaction => {
    if (filter === "all") return true;
    if (filter === "high") return transaction.score >= 0.7;
    if (filter === "medium") return transaction.score >= 0.4 && transaction.score < 0.7;
    if (filter === "low") return transaction.score < 0.4;
    return true;
  });

  // Count transactions by risk level
  const highRiskCount = transactions.filter(t => t.score >= 0.7).length;
  const mediumRiskCount = transactions.filter(t => t.score >= 0.4 && t.score < 0.7).length;
  const lowRiskCount = transactions.filter(t => t.score < 0.4).length;

  // Handle feedback submission
  const handleFeedbackSubmit = (id: string, isCorrect: boolean, feedback?: string) => {
    console.log(`Feedback for transaction ${id}:`, { isCorrect, feedback });
    // In a real app, we would send this to an API
  };

  // Handle CSV download
  const handleDownloadCSV = () => {
    // In a real app, we'd generate a proper CSV file
    // This is just a simple demo implementation
    const headers = ["Transaction ID", "Timestamp", "Amount", "Account", "Type", "Risk Score", "AI Analysis"];
    
    const csvRows = [
      headers.join(","),
      ...transactions.map(t => [
        t.id,
        t.timestamp,
        t.amount,
        t.accountNumber,
        t.transactionType,
        t.score,
        `"${t.reason.replace(/"/g, '""')}"`
      ].join(","))
    ];
    
    const csvContent = csvRows.join("\n");
    
    // Create a blob and download it
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `fraud_log_${new Date().toISOString().split("T")[0]}.csv`);
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    toast.success("CSV file downloaded successfully");
  };

  // Demo refresh function
  const handleRefresh = () => {
    setRefreshing(true);
    // Simulate API call delay
    setTimeout(() => {
      setRefreshing(false);
      toast.success("Dashboard refreshed with latest data");
    }, 1500);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-1 container py-6 px-4">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
          <div>
            <h1 className="text-2xl font-bold">Fraud Detection Dashboard</h1>
            <p className="text-muted-foreground">Monitor and manage suspicious activity</p>
          </div>
          
          <div className="flex gap-2">
            <Button 
              variant="outline" 
              className="gap-1"
              onClick={handleDownloadCSV}
            >
              <FileDown className="h-4 w-4" />
              Export CSV
            </Button>
            
            <Button 
              className="gap-1"
              onClick={handleRefresh}
              disabled={refreshing}
            >
              <RefreshCw className={`h-4 w-4 ${refreshing ? "animate-spin" : ""}`} />
              Refresh
            </Button>
          </div>
        </div>
        
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <Card>
            <CardHeader className="py-4">
              <CardTitle className="text-base flex justify-between items-center">
                <span className="flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-fraud-high" />
                  High Risk
                </span>
                <span className="text-fraud-high font-bold">{highRiskCount}</span>
              </CardTitle>
            </CardHeader>
          </Card>
          
          <Card>
            <CardHeader className="py-4">
              <CardTitle className="text-base flex justify-between items-center">
                <span className="flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-fraud-medium" />
                  Medium Risk
                </span>
                <span className="text-fraud-medium font-bold">{mediumRiskCount}</span>
              </CardTitle>
            </CardHeader>
          </Card>
          
          <Card>
            <CardHeader className="py-4">
              <CardTitle className="text-base flex justify-between items-center">
                <span className="flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-fraud-low" />
                  Low Risk
                </span>
                <span className="text-fraud-low font-bold">{lowRiskCount}</span>
              </CardTitle>
            </CardHeader>
          </Card>
        </div>
        
        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <div className="bg-card rounded-lg border border-border mb-6">
              <div className="p-4 flex flex-col md:flex-row justify-between md:items-center gap-2">
                <h2 className="text-xl font-semibold">Flagged Transactions</h2>
                
                <div className="flex gap-2 items-center">
                  <div className="relative flex items-center">
                    <Search className="absolute left-2.5 h-4 w-4 text-muted-foreground" />
                    <input
                      type="text"
                      placeholder="Search transactions..."
                      className="pl-8 h-9 w-full md:w-[200px] bg-secondary rounded-md text-sm border border-border focus:outline-none focus:ring-1 focus:ring-primary"
                    />
                  </div>
                  
                  <Button variant="outline" size="icon">
                    <Filter className="h-4 w-4" />
                  </Button>
                </div>
              </div>
              
              <Tabs defaultValue="all" className="w-full">
                <div className="px-4 border-b border-border">
                  <TabsList className="bg-transparent">
                    <TabsTrigger value="all" onClick={() => setFilter("all")}>
                      All
                    </TabsTrigger>
                    <TabsTrigger value="high" onClick={() => setFilter("high")}>
                      High Risk
                    </TabsTrigger>
                    <TabsTrigger value="medium" onClick={() => setFilter("medium")}>
                      Medium Risk
                    </TabsTrigger>
                    <TabsTrigger value="low" onClick={() => setFilter("low")}>
                      Low Risk
                    </TabsTrigger>
                  </TabsList>
                </div>
                
                <TabsContent value="all" className="p-0 m-0">
                  <div className="p-4 space-y-4">
                    {filteredTransactions.length > 0 ? (
                      filteredTransactions.map(transaction => (
                        <TransactionCard
                          key={transaction.id}
                          transaction={transaction}
                          onFeedbackSubmit={handleFeedbackSubmit}
                        />
                      ))
                    ) : (
                      <Alert>
                        <AlertTitle>No transactions found</AlertTitle>
                        <AlertDescription>
                          No transactions match your current filter criteria.
                        </AlertDescription>
                      </Alert>
                    )}
                  </div>
                </TabsContent>
                
                {/* All tab content is shown based on the filter state */}
                <TabsContent value="high" className="p-0 m-0"></TabsContent>
                <TabsContent value="medium" className="p-0 m-0"></TabsContent>
                <TabsContent value="low" className="p-0 m-0"></TabsContent>
              </Tabs>
            </div>
          </div>
          
          <div className="space-y-6">
            {/* Risk Distribution Card */}
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-base flex items-center gap-2">
                  <PieChart className="h-4 w-4" />
                  Fraud Risk Distribution
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex justify-center py-4">
                  <ScoreGauge score={0.68} size="lg" showValue={false} />
                </div>
                <div className="grid grid-cols-3 gap-2 text-center pt-2">
                  <div>
                    <div className="h-2 rounded-full bg-fraud-low mb-1"></div>
                    <p className="text-xs text-muted-foreground">Low Risk</p>
                    <p className="text-sm font-medium">{lowRiskCount}</p>
                  </div>
                  <div>
                    <div className="h-2 rounded-full bg-fraud-medium mb-1"></div>
                    <p className="text-xs text-muted-foreground">Medium Risk</p>
                    <p className="text-sm font-medium">{mediumRiskCount}</p>
                  </div>
                  <div>
                    <div className="h-2 rounded-full bg-fraud-high mb-1"></div>
                    <p className="text-xs text-muted-foreground">High Risk</p>
                    <p className="text-sm font-medium">{highRiskCount}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            {/* Recent Activity Card */}
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-base flex items-center gap-2">
                  <Clock className="h-4 w-4" />
                  Recent Activity
                </CardTitle>
              </CardHeader>
              <CardContent className="px-2">
                <div className="space-y-1">
                  <div className="text-xs p-2 hover:bg-secondary rounded flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-fraud-high"></div>
                    <p className="flex-1">High risk transaction detected</p>
                    <p className="text-muted-foreground">4min ago</p>
                  </div>
                  <div className="text-xs p-2 hover:bg-secondary rounded flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-primary"></div>
                    <p className="flex-1">System updated transaction risk models</p>
                    <p className="text-muted-foreground">15min ago</p>
                  </div>
                  <div className="text-xs p-2 hover:bg-secondary rounded flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-fraud-medium"></div>
                    <p className="flex-1">Medium risk transaction flagged</p>
                    <p className="text-muted-foreground">32min ago</p>
                  </div>
                  <div className="text-xs p-2 hover:bg-secondary rounded flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-primary"></div>
                    <p className="flex-1">Admin logged in</p>
                    <p className="text-muted-foreground">45min ago</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            {/* Transaction Volume Card */}
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-base flex items-center gap-2">
                  <BarChart3 className="h-4 w-4" />
                  Transaction Volume
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-32 flex items-end justify-between gap-1 pt-2">
                  {[15, 32, 26, 42, 38, 55, 29].map((value, i) => (
                    <div key={i} className="w-full">
                      <div 
                        className="bg-primary/70 hover:bg-primary rounded-t"
                        style={{ height: `${value * 1.5}px` }}
                      ></div>
                    </div>
                  ))}
                </div>
                <div className="flex justify-between text-xs text-muted-foreground pt-1">
                  <div>Mon</div>
                  <div>Tue</div>
                  <div>Wed</div>
                  <div>Thu</div>
                  <div>Fri</div>
                  <div>Sat</div>
                  <div>Sun</div>
                </div>
              </CardContent>
            </Card>
            
            {/* Feedback Button */}
            <Button 
              variant="outline" 
              className="w-full"
              onClick={() => setFeedbackVisible(true)}
            >
              Provide System Feedback
            </Button>
            
            {/* Feedback Form Modal */}
            {feedbackVisible && (
              <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
                <div className="max-w-lg w-full">
                  <FeedbackForm onClose={() => setFeedbackVisible(false)} />
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;

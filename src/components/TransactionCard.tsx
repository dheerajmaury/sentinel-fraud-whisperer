
import { useState } from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import ScoreGauge from "./ScoreGauge";
import { Separator } from "../components/ui/separator";
import { toast } from "sonner";
import { AlertTriangle, CheckCircle, XCircle, FileText } from "lucide-react";

type TransactionType = "wire" | "card" | "atm" | "online" | "pos";

export interface Transaction {
  id: string;
  timestamp: string;
  amount: number;
  accountNumber: string;
  transactionType: TransactionType;
  score: number;
  reason: string;
}

interface TransactionCardProps {
  transaction: Transaction;
  onFeedbackSubmit: (id: string, isCorrect: boolean, feedback?: string) => void;
}

const TransactionCard = ({ transaction, onFeedbackSubmit }: TransactionCardProps) => {
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedback, setFeedback] = useState("");
  
  const formatDate = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };
  
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
    }).format(amount);
  };
  
  const handleFeedback = (isCorrect: boolean) => {
    if (isCorrect) {
      toast.success("Fraud prediction confirmed");
      onFeedbackSubmit(transaction.id, true);
    } else {
      setShowFeedback(true);
    }
  };
  
  const submitFeedback = () => {
    toast.success("Feedback submitted successfully");
    onFeedbackSubmit(transaction.id, false, feedback);
    setShowFeedback(false);
    setFeedback("");
  };

  return (
    <Card className="border-border/50 bg-card/80 backdrop-blur">
      <CardHeader className="pb-2">
        <div className="flex justify-between items-center">
          <div>
            <CardTitle className="text-lg flex items-center gap-2">
              <AlertTriangle 
                className={`h-5 w-5 ${transaction.score > 0.7 ? 'text-fraud-high' : transaction.score > 0.4 ? 'text-fraud-medium' : 'text-fraud-low'}`} 
              />
              Transaction #{transaction.id}
            </CardTitle>
            <CardDescription>{formatDate(transaction.timestamp)}</CardDescription>
          </div>
          <ScoreGauge score={transaction.score} size="sm" />
        </div>
      </CardHeader>
      
      <CardContent className="pb-2">
        <div className="grid grid-cols-2 gap-2 mb-3">
          <div>
            <p className="text-xs text-muted-foreground">Amount</p>
            <p className="text-sm font-medium">{formatCurrency(transaction.amount)}</p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground">Account</p>
            <p className="text-sm font-medium">
              {"•••• " + transaction.accountNumber.slice(-4)}
            </p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground">Type</p>
            <p className="text-sm font-medium capitalize">{transaction.transactionType}</p>
          </div>
        </div>
        
        <Separator className="my-2" />
        
        <div>
          <p className="text-xs text-muted-foreground mb-1">AI Analysis</p>
          <div className="text-sm bg-secondary/50 p-2 rounded border border-border/50">
            {transaction.reason}
          </div>
        </div>
      </CardContent>
      
      <CardFooter className="flex-col gap-2">
        {!showFeedback ? (
          <div className="flex w-full justify-between gap-2">
            <Button 
              variant="outline" 
              className="w-1/2"
              onClick={() => handleFeedback(false)}
            >
              <XCircle className="h-4 w-4 mr-1" /> Incorrect
            </Button>
            <Button 
              className="w-1/2"
              onClick={() => handleFeedback(true)}
            >
              <CheckCircle className="h-4 w-4 mr-1" /> Correct
            </Button>
          </div>
        ) : (
          <div className="w-full space-y-2">
            <textarea
              className="w-full h-20 p-2 bg-secondary text-sm rounded border border-border resize-none focus:outline-none focus:ring-1 focus:ring-primary"
              placeholder="Please provide feedback on why this prediction is incorrect..."
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
            />
            <div className="flex justify-end gap-2">
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => setShowFeedback(false)}
              >
                Cancel
              </Button>
              <Button 
                size="sm"
                onClick={submitFeedback}
              >
                Submit Feedback
              </Button>
            </div>
          </div>
        )}
      </CardFooter>
    </Card>
  );
};

export default TransactionCard;

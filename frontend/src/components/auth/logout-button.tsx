import { LogOut } from 'lucide-react';
import { logout } from '@/lib/actions';
import { Button } from '../ui/button';

export default function LogoutButton() {
  return (
    <form action={logout}>
      <Button type="submit" variant="outline">
        <LogOut className="mr-2 h-4 w-4" />
        Logout
      </Button>
    </form>
  );
}
